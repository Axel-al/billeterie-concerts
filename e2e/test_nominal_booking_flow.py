from decimal import Decimal

import pytest
from django.urls import reverse
from playwright.sync_api import expect

from orders.models import Order, OrderStatus


@pytest.mark.django_db(transaction=True)
def test_nominal_booking_flow_accepted_payment_appears_in_history(
    page,
    live_server,
    booking_scenario,
):
    page.route("https://cdn.jsdelivr.net/**", lambda route: route.abort())

    concert = booking_scenario.concert
    category = booking_scenario.category
    user = booking_scenario.user

    page.goto(
        f"{live_server.url}{reverse('concerts:list')}",
        wait_until="domcontentloaded",
    )
    catalog_heading = page.get_by_role(
        "heading",
        name="Concerts ouverts à la vente",
    )
    expect(catalog_heading).to_be_visible()
    expect(page.get_by_text(concert.title)).to_be_visible()

    page.get_by_test_id(f"concert-detail-link-{concert.pk}").click()
    expect(page).to_have_url(
        f"{live_server.url}{reverse('concerts:detail', args=[concert.pk])}"
    )
    expect(page.get_by_role("heading", name=concert.title)).to_be_visible()
    expect(page.get_by_text("Ce concert est réservable")).to_be_visible()

    page.get_by_test_id("login-to-book-link").click()
    expect(page.get_by_role("heading", name="Connexion")).to_be_visible()
    page.get_by_test_id("login-email").fill(user.email)
    page.get_by_test_id("login-password").fill(booking_scenario.password)
    page.get_by_test_id("login-submit").click()

    expect(page).to_have_url(
        f"{live_server.url}{reverse('concerts:detail', args=[concert.pk])}"
    )
    expect(page.get_by_test_id("booking-form")).to_be_visible()
    page.get_by_test_id("seat-category-select").select_option(value=str(category.pk))
    page.get_by_test_id("ticket-quantity-input").fill("2")
    page.get_by_test_id("add-to-cart-submit").click()

    expect(page.get_by_role("heading", name="Votre panier")).to_be_visible()
    expect(page.get_by_role("heading", name=concert.title)).to_be_visible()
    expect(page.get_by_test_id("cart-table")).to_contain_text("Fosse")
    expect(page.get_by_test_id("cart-table")).to_contain_text("80,00")

    page.get_by_test_id("cart-checkout-link").click()
    expect(page.get_by_role("heading", name="Valider le panier")).to_be_visible()
    expect(page.get_by_test_id("checkout-table")).to_contain_text("Total à payer")
    expect(page.get_by_test_id("checkout-table")).to_contain_text("80,00")

    page.get_by_test_id("checkout-payment-link").click()
    expect(page.get_by_role("heading", name="Paiement simulé")).to_be_visible()
    page.get_by_test_id("payment-card-number").fill("4242424242424242")
    page.get_by_test_id("payment-submit").click()

    expect(page.get_by_test_id("payment-confirmation")).to_be_visible()
    expect(page.get_by_test_id("payment-confirmation")).to_contain_text(
        "Commande confirmée"
    )
    expect(page.get_by_role("heading", name=concert.title)).to_be_visible()
    expect(page.get_by_test_id("payment-confirmation-table")).to_contain_text("80,00")

    page.get_by_test_id("order-history-link").click()
    expect(page.get_by_role("heading", name="Mes commandes")).to_be_visible()
    expect(page.get_by_test_id("order-history-table")).to_contain_text(concert.title)
    expect(page.get_by_test_id("order-history-table")).to_contain_text("2")
    expect(page.get_by_test_id("order-history-table")).to_contain_text("80,00")

    category.refresh_from_db()
    order = Order.objects.get(user=user, status=OrderStatus.PAID)
    order_line = order.lines.get()

    assert order.total_quantity == 2
    assert order.total_amount == Decimal("80.00")
    assert order_line.category_name_snapshot == "Fosse"
    assert order_line.unit_price == Decimal("40.00")
    assert order_line.quantity == 2
    assert category.stock_remaining == 6
