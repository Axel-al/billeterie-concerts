from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction

from cart.models import Cart, CartLine, CartStatus
from concerts.models import Concert, ConcertStatus, SeatCategory

MIN_TICKETS_PER_CONCERT = 1
MAX_TICKETS_PER_CONCERT = 6


@dataclass(frozen=True)
class CartValidationResult:
    concert: Concert
    lines: tuple[CartLine, ...]
    total_quantity: int


def validate_ticket_quantity(quantity: int) -> None:
    if not isinstance(quantity, int):
        raise ValidationError("La quantite doit etre un entier.")
    if quantity < MIN_TICKETS_PER_CONCERT:
        raise ValidationError("La quantite doit etre au moins egale a 1.")
    if quantity > MAX_TICKETS_PER_CONCERT:
        raise ValidationError("La quantite ne peut pas depasser 6 billets.")


def validate_concert_bookable(concert: Concert) -> None:
    if concert.status == ConcertStatus.CANCELLED:
        raise ValidationError("Le concert annule ne peut pas etre reserve.")
    if concert.status == ConcertStatus.CLOSED:
        raise ValidationError("Les ventes de ce concert sont cloturees.")
    if concert.is_past():
        raise ValidationError("Le concert passe ne peut pas etre reserve.")
    if concert.status != ConcertStatus.OPEN:
        raise ValidationError("Le concert n'est pas ouvert a la vente.")
    if not concert.has_available_stock():
        raise ValidationError("Le concert ne dispose plus de places disponibles.")


def validate_category_stock(seat_category: SeatCategory, quantity: int) -> None:
    validate_ticket_quantity(quantity)
    if not seat_category.has_stock_for(quantity):
        raise ValidationError("Le stock restant est insuffisant.")


def get_or_create_active_cart(user) -> Cart:
    cart, _created = Cart.objects.get_or_create(
        user=user,
        status=CartStatus.ACTIVE,
        defaults={"concert": None},
    )
    return cart


@transaction.atomic
def add_ticket_to_cart(user, seat_category: SeatCategory, quantity: int) -> CartLine:
    validate_ticket_quantity(quantity)

    seat_category = SeatCategory.objects.select_related("concert").get(
        pk=seat_category.pk
    )
    validate_concert_bookable(seat_category.concert)

    cart = get_or_create_active_cart(user)
    cart = Cart.objects.select_for_update().select_related("concert").get(pk=cart.pk)

    if cart.concert_id is None:
        cart.concert = seat_category.concert
        cart.save(update_fields=("concert", "updated_at"))
    elif cart.concert_id != seat_category.concert_id:
        raise ValidationError("Un panier actif ne peut contenir qu'un seul concert.")

    line = CartLine.objects.filter(cart=cart, seat_category=seat_category).first()
    current_line_quantity = line.quantity if line else 0
    new_line_quantity = current_line_quantity + quantity
    validate_ticket_quantity(new_line_quantity)
    validate_category_stock(seat_category, new_line_quantity)

    other_quantity = sum(
        existing_line.quantity
        for existing_line in cart.lines.exclude(seat_category=seat_category)
    )
    total_quantity = other_quantity + new_line_quantity
    validate_ticket_quantity(total_quantity)

    if line is None:
        return CartLine.objects.create(
            cart=cart,
            seat_category=seat_category,
            quantity=quantity,
        )

    line.quantity = new_line_quantity
    line.save(update_fields=("quantity", "updated_at"))
    return line


def validate_cart_for_checkout(cart: Cart) -> CartValidationResult:
    if cart.status != CartStatus.ACTIVE:
        raise ValidationError("Seul un panier actif peut etre valide.")

    lines = tuple(cart.lines.select_related("seat_category__concert").order_by("id"))
    if not lines:
        raise ValidationError("Le panier doit contenir au moins un billet.")

    concert_ids = {line.seat_category.concert_id for line in lines}
    if len(concert_ids) != 1 or cart.concert_id not in concert_ids:
        raise ValidationError("Un panier valide ne peut contenir qu'un seul concert.")

    concert = lines[0].seat_category.concert
    validate_concert_bookable(concert)

    total_quantity = sum(line.quantity for line in lines)
    validate_ticket_quantity(total_quantity)

    for line in lines:
        validate_ticket_quantity(line.quantity)
        validate_category_stock(line.seat_category, line.quantity)

    return CartValidationResult(
        concert=concert,
        lines=lines,
        total_quantity=total_quantity,
    )
