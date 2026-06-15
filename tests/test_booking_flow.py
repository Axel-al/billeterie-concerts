from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from cart.models import Cart, CartLine, CartStatus
from cart.services import add_ticket_to_cart
from concerts.models import Concert, ConcertStatus, SeatCategory
from orders.models import Order, OrderStatus
from payments.models import Payment, PaymentResult
from payments.services import process_simulated_card_payment

VALID_PASSWORD = "MotDePasseTresSolide2026!"


@pytest.fixture(autouse=True)
def frozen_clock():
    with freeze_time("2026-06-14 12:00:00"):
        yield


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        email="client@example.com",
        password=VALID_PASSWORD,
    )


@pytest.fixture
def other_user(db):
    return get_user_model().objects.create_user(
        email="autre-client@example.com",
        password=VALID_PASSWORD,
    )


def create_concert(
    *,
    title="Nuit Electrique",
    status=ConcertStatus.OPEN,
    starts_at=None,
):
    return Concert.objects.create(
        title=title,
        artist="The Validation Keys",
        description="Une soirée de concert à découvrir.",
        starts_at=starts_at or timezone.now() + timedelta(days=30),
        venue="Le Grand Dôme",
        status=status,
    )


def create_category(
    concert,
    *,
    name="Fosse",
    price=Decimal("35.00"),
    stock=10,
):
    return SeatCategory.objects.create(
        concert=concert,
        name=name,
        price=price,
        stock_initial=stock,
        stock_remaining=stock,
    )


def post_add_to_cart(client, concert, category, quantity, *, follow=True):
    return client.post(
        reverse("cart:add_ticket", args=[concert.pk]),
        data={
            "seat_category": category.pk,
            "quantity": quantity,
        },
        follow=follow,
    )


@pytest.mark.django_db
def test_anonymous_user_cannot_access_checkout_or_payment(client):
    checkout_response = client.get(reverse("cart:checkout"))
    payment_response = client.post(
        reverse("payments:simulate"),
        data={"card_number": "4242424242424242"},
    )

    assert checkout_response.status_code == 302
    assert checkout_response["Location"] == (
        f"{reverse('accounts:login')}?next={reverse('cart:checkout')}"
    )
    assert payment_response.status_code == 302
    assert payment_response["Location"] == (
        f"{reverse('accounts:login')}?next={reverse('payments:simulate')}"
    )


@pytest.mark.parametrize(
    ("quantity", "expected_accepted"),
    [
        (0, False),
        (1, True),
        (6, True),
        (7, False),
    ],
)
@pytest.mark.django_db
def test_add_to_cart_quantity_boundaries(client, user, quantity, expected_accepted):
    concert = create_concert()
    category = create_category(concert, stock=10)
    client.force_login(user)

    response = post_add_to_cart(client, concert, category, quantity)

    if expected_accepted:
        line = CartLine.objects.get()
        assert response.redirect_chain[-1][0] == reverse("cart:detail")
        assert line.quantity == quantity
    else:
        assert CartLine.objects.count() == 0
        assert "La quantité" in response.content.decode()


@pytest.mark.django_db
def test_insufficient_stock_is_rejected_through_add_to_cart_flow(client, user):
    concert = create_concert()
    category = create_category(concert, stock=1)
    client.force_login(user)

    response = post_add_to_cart(client, concert, category, 2)

    assert CartLine.objects.count() == 0
    assert "Le stock restant est insuffisant." in response.content.decode()


@pytest.mark.django_db
def test_past_concert_is_rejected_through_add_to_cart_flow(client, user):
    concert = create_concert(starts_at=timezone.now() - timedelta(minutes=1))
    category = create_category(concert)
    client.force_login(user)

    response = post_add_to_cart(client, concert, category, 1)

    assert CartLine.objects.count() == 0
    assert "Le concert passé ne peut pas être réservé." in response.content.decode()


@pytest.mark.django_db
def test_cancelled_concert_is_rejected_through_add_to_cart_flow(client, user):
    concert = create_concert(status=ConcertStatus.CANCELLED)
    category = create_category(concert)
    client.force_login(user)

    response = post_add_to_cart(client, concert, category, 1)

    assert CartLine.objects.count() == 0
    assert "Le concert annulé ne peut pas être réservé." in response.content.decode()


@pytest.mark.django_db
def test_closed_concert_is_rejected_through_add_to_cart_flow(client, user):
    concert = create_concert(status=ConcertStatus.CLOSED)
    category = create_category(concert)
    client.force_login(user)

    response = post_add_to_cart(client, concert, category, 1)

    assert CartLine.objects.count() == 0
    assert "Les ventes de ce concert sont clôturées." in response.content.decode()


@pytest.mark.django_db
def test_cart_display_calculates_total(client, user):
    concert = create_concert()
    fosse = create_category(concert, name="Fosse", price=Decimal("20.00"))
    balcon = create_category(concert, name="Balcon", price=Decimal("30.00"))
    add_ticket_to_cart(user, fosse, 2)
    add_ticket_to_cart(user, balcon, 1)
    client.force_login(user)

    response = client.get(reverse("cart:detail"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Total du panier" in content
    assert "70,00" in content


@pytest.mark.django_db
def test_checkout_page_with_valid_active_cart_displays_checkout_context(client, user):
    concert = create_concert()
    category = create_category(concert, price=Decimal("25.00"))
    add_ticket_to_cart(user, category, 2)
    client.force_login(user)

    response = client.get(reverse("cart:checkout"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Valider le panier" in content
    assert concert.title in content
    assert "Total à payer" in content
    assert "50,00" in content
    assert "Passer au paiement" in content


@pytest.mark.django_db
def test_checkout_page_with_invalid_active_cart_displays_validation_error(
    client,
    user,
):
    concert = create_concert()
    Cart.objects.create(user=user, concert=concert)
    client.force_login(user)

    response = client.get(reverse("cart:checkout"))

    assert response.status_code == 200
    assert "Le panier doit contenir au moins un billet." in response.content.decode()


@pytest.mark.django_db
def test_payment_page_with_valid_active_cart_displays_form_and_total(client, user):
    concert = create_concert()
    category = create_category(concert, price=Decimal("25.00"))
    add_ticket_to_cart(user, category, 2)
    client.force_login(user)

    response = client.get(reverse("payments:simulate"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Paiement simulé" in content
    assert "Numéro de carte" in content
    assert concert.title in content
    assert "Total à payer" in content
    assert "50,00" in content


@pytest.mark.django_db
def test_payment_page_with_no_active_cart_displays_empty_cart_message(client, user):
    client.force_login(user)

    response = client.get(reverse("payments:simulate"))

    assert response.status_code == 200
    assert "Votre panier est vide." in response.content.decode()


@pytest.mark.django_db
def test_payment_page_with_invalid_active_cart_displays_validation_error(
    client,
    user,
):
    concert = create_concert()
    Cart.objects.create(user=user, concert=concert)
    client.force_login(user)

    response = client.get(reverse("payments:simulate"))

    assert response.status_code == 200
    assert "Le panier doit contenir au moins un billet." in response.content.decode()


@pytest.mark.django_db
def test_payment_post_with_no_active_cart_redirects_to_cart_with_error(
    client,
    user,
):
    client.force_login(user)

    response = client.post(
        reverse("payments:simulate"),
        data={"card_number": "4242424242424242"},
        follow=True,
    )

    assert response.redirect_chain[-1][0] == reverse("cart:detail")
    assert "Votre panier est vide." in response.content.decode()


@pytest.mark.django_db
def test_payment_post_when_active_cart_becomes_invalid_redirects_to_checkout(
    client,
    user,
):
    concert = create_concert()
    category = create_category(concert, stock=3)
    add_ticket_to_cart(user, category, 2)
    category.stock_remaining = 1
    category.save(update_fields=("stock_remaining", "updated_at"))
    client.force_login(user)

    response = client.post(
        reverse("payments:simulate"),
        data={"card_number": "4242424242424242"},
        follow=True,
    )

    assert response.redirect_chain[-1][0] == reverse("cart:checkout")
    assert "Le stock restant est insuffisant." in response.content.decode()
    assert Order.objects.count() == 0
    assert Payment.objects.count() == 0


@pytest.mark.django_db
def test_accepted_payment_creates_paid_order_and_decrements_stock(client, user):
    concert = create_concert()
    category = create_category(concert, price=Decimal("40.00"), stock=8)
    line = add_ticket_to_cart(user, category, 2)
    client.force_login(user)

    response = client.post(
        reverse("payments:simulate"),
        data={"card_number": "4242424242424242"},
        follow=True,
    )

    category.refresh_from_db()
    line.cart.refresh_from_db()
    order = Order.objects.get()
    order_line = order.lines.get()
    assert response.redirect_chain[-1][0] == reverse(
        "payments:confirmation",
        args=[order.pk],
    )
    assert "Commande confirmée" in response.content.decode()
    assert Payment.objects.get().result == PaymentResult.ACCEPTED
    assert order.status == OrderStatus.PAID
    assert order.is_final
    assert order.total_amount == Decimal("80.00")
    assert order_line.unit_price == Decimal("40.00")
    assert order_line.category_name_snapshot == "Fosse"
    assert category.stock_remaining == 6
    assert line.cart.status == CartStatus.CHECKED_OUT

    category.price = Decimal("99.00")
    category.save(update_fields=("price", "updated_at"))
    order_line.refresh_from_db()
    assert order_line.unit_price == Decimal("40.00")


@pytest.mark.django_db
def test_refused_payment_does_not_create_validated_order_or_decrement_stock(
    client,
    user,
):
    concert = create_concert()
    category = create_category(concert, price=Decimal("40.00"), stock=8)
    line = add_ticket_to_cart(user, category, 2)
    client.force_login(user)

    response = client.post(
        reverse("payments:simulate"),
        data={"card_number": "4000000000000000"},
        follow=True,
    )

    category.refresh_from_db()
    line.cart.refresh_from_db()
    refused_order = Order.objects.get()
    assert response.redirect_chain[-1][0] == reverse(
        "payments:refused",
        args=[refused_order.pk],
    )
    assert "Paiement refusé. Votre commande n’a pas été validée." in (
        response.content.decode()
    )
    assert Payment.objects.get().result == PaymentResult.REFUSED
    assert refused_order.status == OrderStatus.REFUSED
    assert not refused_order.is_final
    assert Order.objects.filter(status=OrderStatus.PAID).count() == 0
    assert category.stock_remaining == 8
    assert line.cart.status == CartStatus.ACTIVE


@pytest.mark.django_db
def test_user_cannot_access_another_users_cart_checkout_or_order_pages(
    client,
    user,
    other_user,
):
    concert = create_concert()
    category = create_category(concert, stock=8)
    add_ticket_to_cart(user, category, 1)
    accepted_payment = process_simulated_card_payment(
        user.carts.get(status=CartStatus.ACTIVE),
        "4242424242424242",
    )
    add_ticket_to_cart(user, category, 1)
    refused_payment = process_simulated_card_payment(
        user.carts.get(status=CartStatus.ACTIVE),
        "4000000000000000",
    )
    client.force_login(other_user)

    cart_response = client.get(reverse("cart:detail"))
    checkout_response = client.get(reverse("cart:checkout"))
    confirmation_response = client.get(
        reverse("payments:confirmation", args=[accepted_payment.order_id])
    )
    refused_response = client.get(
        reverse("payments:refused", args=[refused_payment.order_id])
    )

    assert cart_response.status_code == 200
    assert "Votre panier est vide." in cart_response.content.decode()
    assert concert.title not in cart_response.content.decode()
    assert checkout_response.status_code == 200
    assert "Votre panier est vide." in checkout_response.content.decode()
    assert concert.title not in checkout_response.content.decode()
    assert confirmation_response.status_code == 404
    assert refused_response.status_code == 404
