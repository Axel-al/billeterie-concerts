from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F

from cart.models import Cart, CartStatus
from cart.services import validate_cart_for_checkout
from concerts.models import SeatCategory
from orders.models import Order, OrderLine, OrderStatus
from payments.models import Payment, PaymentResult

ACCEPTED_SIMULATED_CARD_NUMBER = "4242424242424242"


def simulated_payment_result_for_card(card_number: str) -> str:
    normalized_card_number = "".join(str(card_number).split())
    if normalized_card_number == ACCEPTED_SIMULATED_CARD_NUMBER:
        return PaymentResult.ACCEPTED
    return PaymentResult.REFUSED


def process_simulated_card_payment(cart: Cart, card_number: str) -> Payment:
    return process_simulated_payment(
        cart,
        simulated_payment_result_for_card(card_number),
    )


@transaction.atomic
def process_simulated_payment(cart: Cart, result: str) -> Payment:
    if result not in PaymentResult.values:
        raise ValidationError("Le résultat du paiement simulé est invalide.")

    locked_cart = (
        Cart.objects.select_for_update()
        .select_related("user", "concert")
        .get(pk=cart.pk)
    )
    validation = validate_cart_for_checkout(locked_cart)

    category_ids = [line.seat_category_id for line in validation.lines]
    categories = SeatCategory.objects.select_for_update().in_bulk(category_ids)

    line_snapshots = []
    total_amount = Decimal("0.00")
    for line in validation.lines:
        seat_category = categories[line.seat_category_id]
        if seat_category.concert_id != validation.concert.id:
            raise ValidationError(
                "Un panier valide ne peut contenir qu’un seul concert."
            )
        if seat_category.stock_remaining < line.quantity:
            raise ValidationError("Le stock restant est insuffisant.")

        line_total = seat_category.price * line.quantity
        total_amount += line_total
        line_snapshots.append((line, seat_category))

    order_status = (
        OrderStatus.PAID
        if result == PaymentResult.ACCEPTED
        else OrderStatus.REFUSED
    )
    order = Order.objects.create(
        user=locked_cart.user,
        concert=validation.concert,
        status=order_status,
        total_amount=total_amount,
    )

    for line, seat_category in line_snapshots:
        OrderLine.objects.create(
            order=order,
            seat_category=seat_category,
            category_name_snapshot=seat_category.name,
            unit_price=seat_category.price,
            quantity=line.quantity,
        )

    if result == PaymentResult.ACCEPTED:
        for line, seat_category in line_snapshots:
            updated_count = SeatCategory.objects.filter(
                pk=seat_category.pk,
                stock_remaining__gte=line.quantity,
            ).update(stock_remaining=F("stock_remaining") - line.quantity)
            if updated_count != 1:
                raise ValidationError("Le stock restant est insuffisant.")

        locked_cart.status = CartStatus.CHECKED_OUT
        locked_cart.save(update_fields=("status", "updated_at"))

    return Payment.objects.create(order=order, amount=total_amount, result=result)
