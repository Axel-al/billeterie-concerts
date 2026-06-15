from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.db.models import QuerySet
from django.utils import timezone

from cart.models import Cart, CartLine, CartStatus
from cart.services import (
    add_ticket_to_cart,
    validate_cart_for_checkout,
    validate_concert_bookable,
    validate_ticket_quantity,
)
from concerts.models import Concert, ConcertStatus, SeatCategory
from orders.models import Order, OrderStatus
from payments.models import Payment, PaymentResult
from payments.services import process_simulated_payment


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        email="client@example.com",
        password="mot-de-passe-solide",
    )


def create_concert(
    *,
    title="Nuit de test",
    status=ConcertStatus.OPEN,
    starts_at=None,
):
    return Concert.objects.create(
        title=title,
        artist="Groupe Exemple",
        description="Concert utilise par les tests.",
        starts_at=starts_at or timezone.now() + timedelta(days=30),
        venue="Salle de test",
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


def test_quantity_zero_rejected():
    with pytest.raises(ValidationError):
        validate_ticket_quantity(0)


def test_quantity_one_accepted():
    validate_ticket_quantity(1)


def test_quantity_six_accepted():
    validate_ticket_quantity(6)


def test_quantity_seven_rejected():
    with pytest.raises(ValidationError):
        validate_ticket_quantity(7)


def test_non_integer_quantity_rejected():
    with pytest.raises(ValidationError):
        validate_ticket_quantity("2")


@pytest.mark.django_db
def test_aggregate_quantity_six_accepted_across_categories(user):
    concert = create_concert()
    fosse = create_category(concert, name="Fosse")
    balcon = create_category(concert, name="Balcon")

    first_line = add_ticket_to_cart(user, fosse, 3)
    add_ticket_to_cart(user, balcon, 3)

    validation = validate_cart_for_checkout(first_line.cart)

    assert validation.total_quantity == 6


@pytest.mark.django_db
def test_aggregate_quantity_seven_rejected_across_categories(user):
    concert = create_concert()
    fosse = create_category(concert, name="Fosse")
    balcon = create_category(concert, name="Balcon")

    add_ticket_to_cart(user, fosse, 3)

    with pytest.raises(ValidationError):
        add_ticket_to_cart(user, balcon, 4)


@pytest.mark.django_db
def test_checkout_rejects_preexisting_cart_above_six_tickets(user):
    concert = create_concert()
    fosse = create_category(concert, name="Fosse")
    balcon = create_category(concert, name="Balcon")
    cart = Cart.objects.create(user=user, concert=concert)
    CartLine.objects.create(cart=cart, seat_category=fosse, quantity=4)
    CartLine.objects.create(cart=cart, seat_category=balcon, quantity=3)

    with pytest.raises(ValidationError):
        validate_cart_for_checkout(cart)


@pytest.mark.django_db
def test_checkout_rejects_mixed_concert_cart(user):
    first_concert = create_concert(title="Premier concert")
    second_concert = create_concert(title="Second concert")
    first_category = create_category(first_concert)
    second_category = create_category(second_concert)
    cart = Cart.objects.create(user=user, concert=first_concert)
    CartLine.objects.create(cart=cart, seat_category=first_category, quantity=1)
    CartLine.objects.create(cart=cart, seat_category=second_category, quantity=1)

    with pytest.raises(ValidationError):
        validate_cart_for_checkout(cart)


@pytest.mark.django_db
def test_active_cart_rejects_adding_another_concert(user):
    first_concert = create_concert(title="Premier concert")
    second_concert = create_concert(title="Second concert")
    first_category = create_category(first_concert)
    second_category = create_category(second_concert)

    add_ticket_to_cart(user, first_category, 1)

    with pytest.raises(ValidationError):
        add_ticket_to_cart(user, second_category, 1)


@pytest.mark.django_db
def test_insufficient_stock_rejected(user):
    concert = create_concert()
    category = create_category(concert, stock=1)

    with pytest.raises(ValidationError):
        add_ticket_to_cart(user, category, 2)


@pytest.mark.django_db
def test_exact_stock_accepted(user):
    concert = create_concert()
    category = create_category(concert, stock=6)

    line = add_ticket_to_cart(user, category, 6)

    assert validate_cart_for_checkout(line.cart).total_quantity == 6


@pytest.mark.django_db
def test_adding_same_category_updates_existing_cart_line(user):
    concert = create_concert()
    category = create_category(concert, stock=6)

    line = add_ticket_to_cart(user, category, 2)
    updated_line = add_ticket_to_cart(user, category, 3)

    assert updated_line.pk == line.pk
    assert updated_line.quantity == 5
    assert CartLine.objects.count() == 1


@pytest.mark.django_db
def test_cart_string_quantity_and_line_string(user):
    concert = create_concert()
    category = create_category(concert, name="Balcon")
    line = add_ticket_to_cart(user, category, 2)
    cart = line.cart

    assert str(cart) == f"Panier #{cart.pk} - client@example.com"
    assert cart.total_quantity == 2
    assert str(line) == "2 x Nuit de test - Balcon"


@pytest.mark.django_db
def test_cart_total_amount_uses_current_category_prices(user):
    concert = create_concert()
    fosse = create_category(concert, name="Fosse", price=Decimal("20.00"))
    balcon = create_category(concert, name="Balcon", price=Decimal("30.00"))

    line = add_ticket_to_cart(user, fosse, 2)
    add_ticket_to_cart(user, balcon, 1)

    assert line.cart.total_amount == Decimal("70.00")


@pytest.mark.django_db
def test_past_concert_not_bookable(user):
    concert = create_concert(starts_at=timezone.now() - timedelta(days=1))
    category = create_category(concert)

    assert not concert.is_bookable()
    with pytest.raises(ValidationError):
        add_ticket_to_cart(user, category, 1)


@pytest.mark.django_db
def test_cancelled_concert_not_bookable(user):
    concert = create_concert(status=ConcertStatus.CANCELLED)
    category = create_category(concert)

    assert not concert.is_bookable()
    with pytest.raises(ValidationError):
        add_ticket_to_cart(user, category, 1)


@pytest.mark.django_db
def test_closed_concert_not_bookable(user):
    concert = create_concert(status=ConcertStatus.CLOSED)
    category = create_category(concert)

    assert not concert.is_bookable()
    with pytest.raises(ValidationError):
        add_ticket_to_cart(user, category, 1)


@pytest.mark.django_db
def test_future_open_concert_with_stock_is_bookable():
    concert = create_concert()
    create_category(concert, stock=1)

    assert concert.is_bookable()


@pytest.mark.django_db
def test_draft_concert_not_bookable(user):
    concert = create_concert(status=ConcertStatus.DRAFT)
    category = create_category(concert)

    assert not concert.is_bookable()
    with pytest.raises(ValidationError):
        add_ticket_to_cart(user, category, 1)


@pytest.mark.django_db
def test_future_open_concert_without_stock_not_bookable():
    concert = create_concert()
    create_category(concert, stock=0)

    assert not concert.is_bookable()
    with pytest.raises(ValidationError):
        validate_concert_bookable(concert)


@pytest.mark.django_db
def test_concert_and_category_string_representations():
    concert = create_concert(title="Scene Claire")
    category = create_category(concert, name="Balcon")

    assert str(concert) == "Scene Claire - Groupe Exemple"
    assert str(category) == "Scene Claire - Balcon"


def test_unsaved_concert_has_no_available_stock():
    concert = Concert(
        title="Sans sauvegarde",
        artist="Groupe Exemple",
        starts_at=timezone.now() + timedelta(days=30),
        venue="Salle de test",
        status=ConcertStatus.OPEN,
    )

    assert not concert.has_available_stock()


@pytest.mark.django_db
def test_stock_cannot_become_negative():
    concert = create_concert()
    category = create_category(concert, stock=1)

    with pytest.raises(IntegrityError), transaction.atomic():
        SeatCategory.objects.filter(pk=category.pk).update(stock_remaining=-1)

    category.refresh_from_db()
    assert category.stock_remaining == 1


@pytest.mark.django_db
def test_inactive_cart_rejected_for_checkout(user):
    concert = create_concert()
    category = create_category(concert)
    cart = Cart.objects.create(
        user=user,
        concert=concert,
        status=CartStatus.ABANDONED,
    )
    CartLine.objects.create(cart=cart, seat_category=category, quantity=1)

    with pytest.raises(ValidationError):
        validate_cart_for_checkout(cart)


@pytest.mark.django_db
def test_empty_cart_rejected_for_checkout(user):
    concert = create_concert()
    cart = Cart.objects.create(user=user, concert=concert)

    with pytest.raises(ValidationError):
        validate_cart_for_checkout(cart)


@pytest.mark.django_db
def test_accepted_payment_creates_paid_order_and_decrements_stock(user):
    concert = create_concert()
    category = create_category(concert, price=Decimal("40.00"), stock=8)
    line = add_ticket_to_cart(user, category, 2)

    payment = process_simulated_payment(line.cart, PaymentResult.ACCEPTED)

    category.refresh_from_db()
    line.cart.refresh_from_db()
    order = payment.order
    order_line = order.lines.get()
    assert payment.result == PaymentResult.ACCEPTED
    assert payment.amount == Decimal("80.00")
    assert str(payment) == f"Paiement #{payment.pk} - Accepté"
    assert order.status == OrderStatus.PAID
    assert order.is_final
    assert order.user == user
    assert order.total_amount == Decimal("80.00")
    assert order.total_quantity == 2
    assert order.concert == concert
    assert order_line.unit_price == Decimal("40.00")
    assert order_line.category_name_snapshot == "Fosse"
    assert category.stock_remaining == 6
    assert line.cart.status == CartStatus.CHECKED_OUT


@pytest.mark.django_db
def test_failed_conditional_stock_update_rolls_back_payment(user, monkeypatch):
    concert = create_concert()
    category = create_category(concert, price=Decimal("40.00"), stock=8)
    line = add_ticket_to_cart(user, category, 2)
    original_update = QuerySet.update

    def fail_stock_decrement(queryset, **kwargs):
        if queryset.model is SeatCategory and "stock_remaining" in kwargs:
            return 0
        return original_update(queryset, **kwargs)

    monkeypatch.setattr(QuerySet, "update", fail_stock_decrement)

    with pytest.raises(ValidationError, match="stock restant est insuffisant"):
        process_simulated_payment(line.cart, PaymentResult.ACCEPTED)

    category.refresh_from_db()
    line.cart.refresh_from_db()
    assert category.stock_remaining == 8
    assert line.cart.status == CartStatus.ACTIVE
    assert Order.objects.count() == 0
    assert Payment.objects.count() == 0


@pytest.mark.django_db
def test_invalid_simulated_payment_result_rejected(user):
    concert = create_concert()
    category = create_category(concert)
    line = add_ticket_to_cart(user, category, 1)

    with pytest.raises(ValidationError):
        process_simulated_payment(line.cart, "unknown")


@pytest.mark.django_db
def test_refused_payment_records_refused_order_and_leaves_stock(user):
    concert = create_concert()
    category = create_category(concert, price=Decimal("40.00"), stock=8)
    line = add_ticket_to_cart(user, category, 2)

    payment = process_simulated_payment(line.cart, PaymentResult.REFUSED)

    category.refresh_from_db()
    line.cart.refresh_from_db()
    order = payment.order
    assert payment.result == PaymentResult.REFUSED
    assert payment.amount == Decimal("80.00")
    assert order.status == OrderStatus.REFUSED
    assert not order.is_final
    assert category.stock_remaining == 8
    assert line.cart.status == CartStatus.ACTIVE


@pytest.mark.django_db
def test_price_snapshot_is_kept_after_category_price_changes(user):
    concert = create_concert()
    category = create_category(concert, price=Decimal("25.00"), stock=8)
    line = add_ticket_to_cart(user, category, 2)

    payment = process_simulated_payment(line.cart, PaymentResult.ACCEPTED)
    category.price = Decimal("99.00")
    category.save(update_fields=("price", "updated_at"))

    order_line = payment.order.lines.get()
    assert order_line.unit_price == Decimal("25.00")
    assert order_line.line_total == Decimal("50.00")


@pytest.mark.django_db
def test_order_and_order_line_string_representations(user):
    concert = create_concert()
    category = create_category(concert, name="Fosse")
    line = add_ticket_to_cart(user, category, 2)
    payment = process_simulated_payment(line.cart, PaymentResult.ACCEPTED)
    order = payment.order
    order_line = order.lines.get()

    assert str(order) == f"Commande #{order.pk} - client@example.com"
    assert str(order_line) == "2 x Fosse"


@pytest.mark.django_db
def test_seed_demo_data_command_is_idempotent():
    call_command("seed_demo_data")
    call_command("seed_demo_data")

    assert Concert.objects.count() == 3
    assert SeatCategory.objects.count() == 7
    assert Concert.objects.filter(status=ConcertStatus.OPEN).count() == 1
    assert Concert.objects.filter(status=ConcertStatus.CANCELLED).count() == 1
    assert Concert.objects.filter(status=ConcertStatus.FINISHED).count() == 1
