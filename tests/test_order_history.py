from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from cart.services import add_ticket_to_cart
from concerts.models import Concert, ConcertStatus, SeatCategory
from orders.models import Order, OrderStatus
from payments.models import PaymentResult
from payments.services import process_simulated_payment

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


def create_concert(*, title="Nuit Electrique"):
    return Concert.objects.create(
        title=title,
        artist="The Validation Keys",
        description="Une soiree de concert a decouvrir.",
        starts_at=timezone.now() + timedelta(days=30),
        venue="Le Grand Dome",
        status=ConcertStatus.OPEN,
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


def create_order(
    user,
    *,
    title="Nuit Electrique",
    category_name="Fosse",
    price=Decimal("35.00"),
    quantity=2,
    result=PaymentResult.ACCEPTED,
    stock=10,
):
    concert = create_concert(title=title)
    category = create_category(
        concert,
        name=category_name,
        price=price,
        stock=stock,
    )
    line = add_ticket_to_cart(user, category, quantity)
    payment = process_simulated_payment(line.cart, result)
    return payment.order, category


@pytest.mark.django_db
def test_anonymous_order_history_and_detail_access_redirect_to_login(client, user):
    order, _category = create_order(user)

    history_response = client.get(reverse("orders:list"))
    detail_response = client.get(reverse("orders:detail", args=[order.pk]))

    assert history_response.status_code == 302
    assert history_response["Location"] == (
        f"{reverse('accounts:login')}?next={reverse('orders:list')}"
    )
    assert detail_response.status_code == 302
    assert detail_response["Location"] == (
        f"{reverse('accounts:login')}?next="
        f"{reverse('orders:detail', args=[order.pk])}"
    )


@pytest.mark.django_db
def test_user_sees_only_their_own_paid_orders(client, user, other_user):
    own_order, _own_category = create_order(user, title="Nuit personnelle")
    other_order, _other_category = create_order(other_user, title="Nuit voisine")
    refused_order, _refused_category = create_order(
        user,
        title="Tentative refusee",
        result=PaymentResult.REFUSED,
    )
    client.force_login(user)

    response = client.get(reverse("orders:list"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Nuit personnelle" in content
    assert reverse("orders:detail", args=[own_order.pk]) in content
    assert "Nuit voisine" not in content
    assert reverse("orders:detail", args=[other_order.pk]) not in content
    assert "Tentative refusee" not in content
    assert reverse("orders:detail", args=[refused_order.pk]) not in content


@pytest.mark.django_db
def test_user_cannot_access_another_users_paid_order_detail(
    client,
    user,
    other_user,
):
    other_order, _category = create_order(other_user)
    client.force_login(user)

    response = client.get(reverse("orders:detail", args=[other_order.pk]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_paid_order_appears_in_history_after_successful_payment(client, user):
    concert = create_concert(title="Apres Paiement")
    category = create_category(concert, price=Decimal("40.00"), stock=8)
    add_ticket_to_cart(user, category, 2)
    client.force_login(user)

    payment_response = client.post(
        reverse("payments:simulate"),
        data={"card_number": "4242424242424242"},
        follow=True,
    )
    order = Order.objects.get(user=user, status=OrderStatus.PAID)
    history_response = client.get(reverse("orders:list"))

    payment_content = payment_response.content.decode()
    history_content = history_response.content.decode()
    assert payment_response.redirect_chain[-1][0] == reverse(
        "payments:confirmation",
        args=[order.pk],
    )
    assert reverse("orders:detail", args=[order.pk]) in payment_content
    assert reverse("orders:list") in payment_content
    assert history_response.status_code == 200
    assert "Apres Paiement" in history_content
    assert "80,00" in history_content


@pytest.mark.django_db
def test_order_detail_displays_consistent_paid_order_data(client, user):
    order, category = create_order(
        user,
        title="Detail Stable",
        category_name="Balcon",
        price=Decimal("42.50"),
        quantity=2,
    )
    category.name = "Categorie modifiee"
    category.price = Decimal("99.00")
    category.save(update_fields=("name", "price", "updated_at"))
    client.force_login(user)

    response = client.get(reverse("orders:detail", args=[order.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Commande #" in content
    assert "14/06/2026" in content
    assert "Payée" in content
    assert "Detail Stable" in content
    assert "Balcon" in content
    assert "Quantité" in content
    assert ">2<" in content
    assert "42,50" in content
    assert "85,00" in content
    assert "Categorie modifiee" not in content
    assert "99,00" not in content


@pytest.mark.django_db
def test_refused_orders_remain_non_final_and_are_excluded_from_history(
    client,
    user,
):
    refused_order, category = create_order(
        user,
        title="Paiement Refusé",
        price=Decimal("40.00"),
        quantity=2,
        result=PaymentResult.REFUSED,
        stock=8,
    )
    category.refresh_from_db()
    refused_order.refresh_from_db()
    client.force_login(user)

    history_response = client.get(reverse("orders:list"))
    detail_response = client.get(reverse("orders:detail", args=[refused_order.pk]))

    assert refused_order.status == OrderStatus.REFUSED
    assert refused_order.payment.result == PaymentResult.REFUSED
    assert not refused_order.is_final
    assert category.stock_remaining == 8
    assert history_response.status_code == 200
    assert "Paiement Refusé" not in history_response.content.decode()
    assert detail_response.status_code == 404
