from html.parser import HTMLParser
from pathlib import Path

TEMPLATE_ROOT = Path(__file__).resolve().parents[1] / "templates"
BOOTSTRAP_CSS_URL = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
BOOTSTRAP_CSS_INTEGRITY = (
    "sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
)
BOOTSTRAP_JS_URL = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)
BOOTSTRAP_JS_INTEGRITY = (
    "sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
)


class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def parse_template(path):
    parser = TagCollector()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.tags


def test_bootstrap_cdn_resources_have_integrity_metadata():
    tags = parse_template(TEMPLATE_ROOT / "base.html")
    resource_tags = {
        attrs.get("href") or attrs.get("src"): attrs
        for tag, attrs in tags
        if tag in {"link", "script"}
    }

    assert resource_tags[BOOTSTRAP_CSS_URL]["integrity"] == BOOTSTRAP_CSS_INTEGRITY
    assert resource_tags[BOOTSTRAP_CSS_URL]["crossorigin"] == "anonymous"
    assert resource_tags[BOOTSTRAP_JS_URL]["integrity"] == BOOTSTRAP_JS_INTEGRITY
    assert resource_tags[BOOTSTRAP_JS_URL]["crossorigin"] == "anonymous"


def test_static_template_messages_do_not_use_status_role():
    status_roles = []

    for template_path in TEMPLATE_ROOT.rglob("*.html"):
        for tag, attrs in parse_template(template_path):
            if attrs.get("role") == "status":
                status_roles.append(f"{template_path.relative_to(TEMPLATE_ROOT)}:{tag}")

    assert status_roles == []
