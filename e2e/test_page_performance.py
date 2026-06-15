import base64
import hashlib
import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from urllib.parse import urljoin

import pytest
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect

LCP_THRESHOLD_MS = 2_000
DESKTOP_VIEWPORT = {"width": 1366, "height": 768}
BOOTSTRAP_FIXTURE_DIR = Path(__file__).parent / "fixtures" / "bootstrap-5.3.3"
CDN_REPLAY_MODE = "local Bootstrap 5.3.3 fixtures matching template SRI hashes"

PERFORMANCE_OBSERVER_SCRIPT = """
(() => {
  window.__enf2LcpEntries = [];
  try {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        window.__enf2LcpEntries.push({
          startTime: entry.startTime,
          renderTime: entry.renderTime,
          loadTime: entry.loadTime,
          size: entry.size,
          element: entry.element ? entry.element.tagName : null,
          url: entry.url || null
        });
      }
    });
    observer.observe({ type: "largest-contentful-paint", buffered: true });
    window.__enf2LcpObserverReady = true;
  } catch (error) {
    window.__enf2LcpObserverError = String(error);
  }
})();
"""

READ_BROWSER_TIMINGS_SCRIPT = """
async () => {
  if (document.fonts && document.fonts.ready) {
    try {
      await document.fonts.ready;
    } catch (error) {
      window.__enf2FontsReadyError = String(error);
    }
  }
  await new Promise((resolve) => {
    requestAnimationFrame(() => requestAnimationFrame(resolve));
  });

  const navigation = performance.getEntriesByType("navigation")[0] || null;
  const lcpEntries = window.__enf2LcpEntries || [];
  const lcpEntry = lcpEntries.length ? lcpEntries[lcpEntries.length - 1] : null;
  const rounded = (value) => (
    Number.isFinite(value) ? Math.round(value * 10) / 10 : null
  );

  return {
    lcpMs: lcpEntry ? rounded(lcpEntry.startTime) : null,
    lcpEntry,
    lcpEntryCount: lcpEntries.length,
    observerReady: window.__enf2LcpObserverReady || false,
    observerError: window.__enf2LcpObserverError || null,
    fontsReadyError: window.__enf2FontsReadyError || null,
    navigation: navigation ? {
      domContentLoadedMs: rounded(
        navigation.domContentLoadedEventEnd - navigation.startTime
      ),
      loadDurationMs: rounded(navigation.loadEventEnd - navigation.startTime),
      responseEndMs: rounded(navigation.responseEnd - navigation.startTime),
      transferSize: navigation.transferSize
    } : null
  };
}
"""


@dataclass(frozen=True)
class BootstrapAsset:
    url: str
    path: Path
    content_type: str
    sha384_digest: str


@cache
def _bootstrap_assets_by_url() -> dict[str, BootstrapAsset]:
    assets = (
        BootstrapAsset(
            url="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/"
            "bootstrap.min.css",
            path=BOOTSTRAP_FIXTURE_DIR / "bootstrap.min.css",
            content_type="text/css",
            sha384_digest=(
                "QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
            ),
        ),
        BootstrapAsset(
            url="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/"
            "bootstrap.bundle.min.js",
            path=BOOTSTRAP_FIXTURE_DIR / "bootstrap.bundle.min.js",
            content_type="application/javascript",
            sha384_digest=(
                "YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
            ),
        ),
    )

    for asset in assets:
        content = asset.path.read_bytes()
        digest = base64.b64encode(hashlib.sha384(content).digest()).decode("ascii")
        assert digest == asset.sha384_digest, (
            f"Bootstrap fixture {asset.path} does not match expected SRI digest. "
            f"Expected {asset.sha384_digest}, got {digest}."
        )

    return {asset.url: asset for asset in assets}


def _install_bootstrap_cdn_replay(context):
    assets_by_url = _bootstrap_assets_by_url()

    def fulfill_from_fixture(route):
        request_url = route.request.url.split("?", 1)[0]
        asset = assets_by_url.get(request_url)
        if asset is None:
            route.fulfill(
                status=404,
                body=f"Unexpected CDN asset in ENF2 performance test: {request_url}",
                content_type="text/plain",
            )
            return

        route.fulfill(
            status=200,
            path=str(asset.path),
            content_type=asset.content_type,
            headers={
                "access-control-allow-origin": "*",
                "cache-control": "public, max-age=31536000, immutable",
            },
        )

    context.route("https://cdn.jsdelivr.net/**", fulfill_from_fixture)


def _authenticated_session_cookie(live_server_url, user):
    session = SessionStore()
    session["_auth_user_id"] = str(user.pk)
    session["_auth_user_backend"] = "django.contrib.auth.backends.ModelBackend"
    session["_auth_user_hash"] = user.get_session_auth_hash()
    session.save()

    return {
        "name": settings.SESSION_COOKIE_NAME,
        "value": session.session_key,
        "url": live_server_url,
        "httpOnly": True,
        "sameSite": "Lax",
    }


def _page_path(page_name, scenario):
    if page_name == "homepage":
        return reverse("home")
    if page_name == "catalog":
        return reverse("concerts:list")
    if page_name == "concert_detail":
        return reverse("concerts:detail", args=[scenario.concert.pk])
    if page_name == "order_history":
        return reverse("orders:list")
    raise AssertionError(f"Unknown ENF2 page name: {page_name}")


def _wait_for_main_content(page, page_name, scenario):
    if page_name == "homepage":
        expect(
            page.get_by_role(
                "heading",
                name="Bienvenue sur la billetterie de concerts",
            )
        ).to_be_visible()
    elif page_name == "catalog":
        expect(
            page.get_by_role("heading", name="Concerts ouverts à la vente")
        ).to_be_visible()
        expect(page.get_by_text(scenario.concert.title)).to_be_visible()
    elif page_name == "concert_detail":
        expect(page.get_by_role("heading", name=scenario.concert.title)).to_be_visible()
        expect(page.get_by_text("Catégories de places")).to_be_visible()
    elif page_name == "order_history":
        expect(page.get_by_role("heading", name="Mes commandes")).to_be_visible()
        expect(page.get_by_test_id("order-history-table")).to_contain_text(
            scenario.concert.title
        )
    else:
        raise AssertionError(f"Unknown ENF2 page name: {page_name}")


def _wait_for_lcp_entry(page):
    try:
        page.wait_for_function(
            "() => (window.__enf2LcpEntries || []).length > 0",
            timeout=LCP_THRESHOLD_MS,
            polling=25,
        )
    except PlaywrightTimeoutError:
        pass


def _diagnostic(page_name, url, metrics):
    return (
        f"ENF2 performance failure for {page_name} ({url}). "
        f"Observed LCP={metrics.get('lcpMs')} ms, "
        f"threshold={LCP_THRESHOLD_MS} ms, "
        f"navigation={json.dumps(metrics.get('navigation'), sort_keys=True)}, "
        f"viewport={DESKTOP_VIEWPORT['width']}x{DESKTOP_VIEWPORT['height']}, "
        f"cdn={CDN_REPLAY_MODE}, "
        f"lcpEntryCount={metrics.get('lcpEntryCount')}, "
        f"observerReady={metrics.get('observerReady')}, "
        f"observerError={metrics.get('observerError')}, "
        f"lcpEntry={json.dumps(metrics.get('lcpEntry'), sort_keys=True)}"
    )


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    "page_name",
    ("homepage", "catalog", "concert_detail", "order_history"),
)
def test_standard_page_lcp_under_two_seconds(
    browser,
    browser_name,
    live_server,
    performance_scenario,
    page_name,
):
    if browser_name != "chromium":
        pytest.skip("ENF2 performance evidence is defined for Playwright Chromium.")

    context = browser.new_context(viewport=DESKTOP_VIEWPORT)
    try:
        _install_bootstrap_cdn_replay(context)
        context.add_init_script(PERFORMANCE_OBSERVER_SCRIPT)
        if page_name == "order_history":
            context.add_cookies(
                [
                    _authenticated_session_cookie(
                        live_server.url,
                        performance_scenario.user,
                    )
                ]
            )

        page = context.new_page()
        url = urljoin(live_server.url, _page_path(page_name, performance_scenario))
        page.goto(url, wait_until="load")
        _wait_for_main_content(page, page_name, performance_scenario)
        _wait_for_lcp_entry(page)
        metrics = page.evaluate(READ_BROWSER_TIMINGS_SCRIPT)
    finally:
        context.close()

    diagnostic = _diagnostic(page_name, url, metrics)
    print(
        "ENF2 performance "
        f"page={page_name} "
        f"url={url} "
        f"lcp_ms={metrics.get('lcpMs')} "
        f"load_duration_ms="
        f"{(metrics.get('navigation') or {}).get('loadDurationMs')} "
        f"dom_content_loaded_ms="
        f"{(metrics.get('navigation') or {}).get('domContentLoadedMs')} "
        f"viewport={DESKTOP_VIEWPORT['width']}x{DESKTOP_VIEWPORT['height']} "
        f"cdn={CDN_REPLAY_MODE}"
    )
    assert metrics["lcpMs"] is not None, diagnostic
    assert metrics["lcpMs"] <= LCP_THRESHOLD_MS, diagnostic
