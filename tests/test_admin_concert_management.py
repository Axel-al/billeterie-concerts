from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib import admin as django_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import ValidationError
from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from cart.models import CartStatus
from cart.services import add_ticket_to_cart
from concerts.admin import ConcertAdmin
from concerts.models import Concert, ConcertStatus, SeatCategory
from orders.admin import OrderAdmin, OrderLineAdmin, OrderLineInline
from orders.models import Order, OrderLine, OrderStatus
from payments.admin import PaymentAdmin
from payments.models import Payment, PaymentResult
from payments.services import process_simulated_payment

VALID_PASSWORD = "MotDePasseTresSolide2026!"


@pytest.fixture(autouse=True)
def frozen_clock():
    with freeze_time("2026-06-14 12:00:00"):
        yield


@pytest.fixture
def standard_user(db):
    return get_user_model().objects.create_user(
        email="client@example.com",
        password=VALID_PASSWORD,
    )


@pytest.fixture
def manager_user(db):
    user = get_user_model().objects.create_user(
        email="gestion@example.com",
        password=VALID_PASSWORD,
    )
    return user


def grant_permissions(user, *permissions):
    for permission in permissions:
        app_label, codename = permission.split(".")
        user.user_permissions.add(
            Permission.objects.get(
                content_type__app_label=app_label,
                codename=codename,
            ),
        )


def create_concert(
    *,
    title="Nuit Administration",
    status=ConcertStatus.OPEN,
):
    return Concert.objects.create(
        title=title,
        artist="The Validation Keys",
        description="Concert de test pour l'administration.",
        starts_at=timezone.now() + timedelta(days=30),
        venue="Le Grand Dome",
        status=status,
    )


def create_category(
    concert,
    *,
    name="Fosse",
    price=Decimal("40.00"),
    stock=10,
):
    return SeatCategory.objects.create(
        concert=concert,
        name=name,
        price=price,
        stock_initial=stock,
        stock_remaining=stock,
    )


def create_paid_order(user, concert, category, quantity=2):
    line = add_ticket_to_cart(user, category, quantity)
    payment = process_simulated_payment(line.cart, PaymentResult.ACCEPTED)
    return payment.order


def build_admin_action_request():
    request = RequestFactory().get("/")
    request.session = {}
    request._messages = FallbackStorage(request)
    return request


@pytest.mark.django_db
def test_sales_overview_permission_rules(client, standard_user, manager_user):
    concert = create_concert()
    create_category(concert)
    url = reverse("concerts:admin_sales_overview")

    anonymous_response = client.get(url)
    assert anonymous_response.status_code == 302
    assert anonymous_response["Location"] == (
        f"{reverse('accounts:login')}?next={url}"
    )

    client.force_login(standard_user)
    standard_response = client.get(url)
    assert standard_response.status_code == 403

    grant_permissions(manager_user, "concerts.view_concert", "orders.view_order")
    client.force_login(manager_user)
    manager_response = client.get(url)

    assert manager_response.status_code == 200
    assert "Administration des ventes" in manager_response.content.decode()
    assert concert.title in manager_response.content.decode()


@pytest.mark.django_db
def test_cancel_action_permission_rules(client, standard_user, manager_user):
    concert = create_concert()
    create_category(concert)
    url = reverse("concerts:admin_cancel", args=[concert.pk])

    anonymous_response = client.post(url)
    assert anonymous_response.status_code == 302
    assert anonymous_response["Location"] == (
        f"{reverse('accounts:login')}?next={url}"
    )

    client.force_login(standard_user)
    standard_response = client.post(url)
    assert standard_response.status_code == 403
    concert.refresh_from_db()
    assert concert.status == ConcertStatus.OPEN

    grant_permissions(manager_user, "concerts.change_concert")
    client.force_login(manager_user)
    manager_response = client.post(url)
    concert.refresh_from_db()

    assert manager_response.status_code == 302
    assert manager_response["Location"] == reverse("concerts:admin_sales_overview")
    assert concert.status == ConcertStatus.CANCELLED


@pytest.mark.django_db
def test_cancelled_concert_rejects_new_reservations_and_preserves_paid_order(
    client,
    standard_user,
    manager_user,
):
    concert = create_concert()
    category = create_category(concert, stock=8)
    order = create_paid_order(standard_user, concert, category, quantity=2)
    category.refresh_from_db()
    stock_after_payment = category.stock_remaining
    grant_permissions(manager_user, "concerts.change_concert")
    client.force_login(manager_user)

    response = client.post(reverse("concerts:admin_cancel", args=[concert.pk]))

    concert.refresh_from_db()
    category.refresh_from_db()
    assert response.status_code == 302
    assert concert.status == ConcertStatus.CANCELLED
    assert category.stock_remaining == stock_after_payment
    with pytest.raises(ValidationError):
        add_ticket_to_cart(standard_user, category, 1)

    client.force_login(standard_user)
    detail_response = client.get(reverse("orders:detail", args=[order.pk]))
    assert detail_response.status_code == 200
    assert concert.title in detail_response.content.decode()


@pytest.mark.django_db
def test_closed_concert_rejects_new_reservations_and_keeps_stock(
    client,
    standard_user,
    manager_user,
):
    concert = create_concert()
    category = create_category(concert, stock=6)
    grant_permissions(manager_user, "concerts.change_concert")
    client.force_login(manager_user)

    response = client.post(reverse("concerts:admin_close", args=[concert.pk]))

    concert.refresh_from_db()
    category.refresh_from_db()
    assert response.status_code == 302
    assert concert.status == ConcertStatus.CLOSED
    assert category.stock_remaining == 6
    with pytest.raises(ValidationError):
        add_ticket_to_cart(standard_user, category, 1)


@pytest.mark.django_db
def test_sales_overview_counts_paid_sales_only(
    client,
    standard_user,
    manager_user,
):
    concert = create_concert(title="Ventes Payées")
    category = create_category(concert, stock=10)
    create_paid_order(standard_user, concert, category, quantity=2)
    refused_line = add_ticket_to_cart(standard_user, category, 3)
    process_simulated_payment(refused_line.cart, PaymentResult.REFUSED)
    category.refresh_from_db()
    grant_permissions(manager_user, "concerts.view_concert", "orders.view_order")
    client.force_login(manager_user)

    response = client.get(reverse("concerts:admin_sales_overview"))

    content = response.content.decode()
    refused_order = Order.objects.get(status=OrderStatus.REFUSED)
    assert response.status_code == 200
    assert refused_order.payment.result == PaymentResult.REFUSED
    assert refused_line.cart.status == CartStatus.ACTIVE
    assert "Ventes Payées" in content
    assert ">1<" in content
    assert ">2<" in content
    assert "80,00" in content
    assert ">10<" in content
    assert ">8<" in content


@pytest.mark.django_db
def test_django_admin_can_create_and_modify_concert_with_category(client):
    admin_user = get_user_model().objects.create_superuser(
        email="admin@example.com",
        password=VALID_PASSWORD,
    )
    client.force_login(admin_user)
    add_url = reverse("admin:concerts_concert_add")

    add_response = client.post(
        add_url,
        data={
            "title": "Creation Admin",
            "artist": "Admin Band",
            "description": "Cree depuis Django admin.",
            "starts_at_0": "2026-07-14",
            "starts_at_1": "20:00:00",
            "venue": "Salle Admin",
            "status": ConcertStatus.OPEN,
            "seat_categories-TOTAL_FORMS": "1",
            "seat_categories-INITIAL_FORMS": "0",
            "seat_categories-MIN_NUM_FORMS": "0",
            "seat_categories-MAX_NUM_FORMS": "1000",
            "seat_categories-0-name": "Balcon",
            "seat_categories-0-price": "35.00",
            "seat_categories-0-stock_initial": "50",
            "seat_categories-0-stock_remaining": "50",
            "seat_categories-0-id": "",
            "seat_categories-0-concert": "",
            "_save": "Enregistrer",
        },
    )

    concert = Concert.objects.get(title="Creation Admin")
    category = concert.seat_categories.get()
    assert add_response.status_code == 302
    assert concert.status == ConcertStatus.OPEN
    assert category.name == "Balcon"
    assert category.stock_initial == 50
    assert category.stock_remaining == 50

    change_response = client.post(
        reverse("admin:concerts_concert_change", args=[concert.pk]),
        data={
            "title": "Creation Admin Modifiee",
            "artist": "Admin Band",
            "description": "Modifie depuis Django admin.",
            "starts_at_0": "2026-07-14",
            "starts_at_1": "21:00:00",
            "venue": "Salle Admin",
            "status": ConcertStatus.CLOSED,
            "seat_categories-TOTAL_FORMS": "1",
            "seat_categories-INITIAL_FORMS": "1",
            "seat_categories-MIN_NUM_FORMS": "0",
            "seat_categories-MAX_NUM_FORMS": "1000",
            "seat_categories-0-name": "Balcon",
            "seat_categories-0-price": "39.00",
            "seat_categories-0-stock_initial": "60",
            "seat_categories-0-stock_remaining": "55",
            "seat_categories-0-id": str(category.pk),
            "seat_categories-0-concert": str(concert.pk),
            "_save": "Enregistrer",
        },
    )

    concert.refresh_from_db()
    category.refresh_from_db()
    assert change_response.status_code == 302
    assert concert.title == "Creation Admin Modifiee"
    assert concert.status == ConcertStatus.CLOSED
    assert category.price == Decimal("39.00")
    assert category.stock_initial == 60
    assert category.stock_remaining == 55


@pytest.mark.django_db
def test_django_admin_uses_french_site_app_and_model_labels(client):
    admin_user = get_user_model().objects.create_superuser(
        email="admin-labels@example.com",
        password=VALID_PASSWORD,
    )
    client.force_login(admin_user)

    response = client.get(reverse("admin:index"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Administration de la billetterie" in content
    assert "Gestion de la billetterie" in content
    for label in (
        "Comptes",
        "Concerts",
        "Paniers",
        "Commandes",
        "Paiements",
        "Utilisateurs",
        "Catégories de places",
        "Lignes de panier",
        "Lignes de commande",
    ):
        assert label in content


@pytest.mark.django_db
def test_concert_admin_metrics_and_bulk_actions(standard_user):
    concert = create_concert(title="Synthèse Admin")
    category = create_category(concert, stock=10)
    create_paid_order(standard_user, concert, category, quantity=2)
    refused_line = add_ticket_to_cart(standard_user, category, 1)
    process_simulated_payment(refused_line.cart, PaymentResult.REFUSED)
    category.refresh_from_db()
    concert_admin = ConcertAdmin(Concert, django_admin.site)

    assert concert_admin.total_stock_initial(concert) == 10
    assert concert_admin.total_stock_remaining(concert) == 8
    assert concert_admin.paid_orders_count(concert) == 1
    assert concert_admin.paid_tickets_sold(concert) == 2
    assert concert_admin.paid_revenue(concert) == Decimal("80.00")

    concert_to_cancel = create_concert(title="Annulation Admin")
    create_category(concert_to_cancel)
    concert_admin.cancel_selected_concerts(
        build_admin_action_request(),
        Concert.objects.filter(pk=concert_to_cancel.pk),
    )
    concert_to_cancel.refresh_from_db()
    assert concert_to_cancel.status == ConcertStatus.CANCELLED

    concert_to_close = create_concert(title="Cloture Admin")
    create_category(concert_to_close)
    concert_admin.close_selected_concerts(
        build_admin_action_request(),
        Concert.objects.filter(pk=concert_to_close.pk),
    )
    concert_to_close.refresh_from_db()
    assert concert_to_close.status == ConcertStatus.CLOSED


def test_order_and_payment_admin_records_are_read_only():
    request = RequestFactory().get("/")

    assert (
        OrderLineInline(Order, django_admin.site).has_add_permission(request)
        is False
    )
    assert OrderAdmin(Order, django_admin.site).has_add_permission(request) is False
    assert (
        OrderAdmin(Order, django_admin.site).has_delete_permission(request)
        is False
    )
    assert (
        OrderLineAdmin(OrderLine, django_admin.site).has_add_permission(request)
        is False
    )
    assert (
        OrderLineAdmin(OrderLine, django_admin.site).has_delete_permission(request)
        is False
    )
    assert PaymentAdmin(Payment, django_admin.site).has_add_permission(request) is False
    assert (
        PaymentAdmin(Payment, django_admin.site).has_delete_permission(request)
        is False
    )
