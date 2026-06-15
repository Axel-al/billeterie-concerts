from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from concerts.models import Concert, SeatCategory


class CartStatus(models.TextChoices):
    ACTIVE = "active", "Actif"
    CHECKED_OUT = "checked_out", "Validé"
    ABANDONED = "abandoned", "Abandonné"


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="utilisateur",
    )
    concert = models.ForeignKey(
        Concert,
        on_delete=models.PROTECT,
        related_name="carts",
        verbose_name="concert",
        null=True,
        blank=True,
    )
    status = models.CharField(
        "statut",
        max_length=20,
        choices=CartStatus.choices,
        default=CartStatus.ACTIVE,
    )
    created_at = models.DateTimeField("date de création", auto_now_add=True)
    updated_at = models.DateTimeField("date de mise à jour", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "panier"
        verbose_name_plural = "paniers"
        constraints = [
            models.UniqueConstraint(
                fields=("user",),
                condition=Q(status=CartStatus.ACTIVE),
                name="unique_active_cart_per_user",
            )
        ]

    def __str__(self) -> str:
        return f"Panier #{self.pk} - {self.user}"

    @property
    def total_quantity(self) -> int:
        return sum(line.quantity for line in self.lines.all())

    @property
    def total_amount(self) -> Decimal:
        return sum(
            (line.line_total for line in self.lines.select_related("seat_category")),
            Decimal("0.00"),
        )


class CartLine(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="lines",
        verbose_name="panier",
    )
    seat_category = models.ForeignKey(
        SeatCategory,
        on_delete=models.PROTECT,
        related_name="cart_lines",
        verbose_name="catégorie de place",
    )
    quantity = models.PositiveSmallIntegerField(
        "quantité",
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    created_at = models.DateTimeField("date de création", auto_now_add=True)
    updated_at = models.DateTimeField("date de mise à jour", auto_now=True)

    class Meta:
        ordering = ("id",)
        verbose_name = "ligne de panier"
        verbose_name_plural = "lignes de panier"
        constraints = [
            models.UniqueConstraint(
                fields=("cart", "seat_category"),
                name="unique_cart_line_per_seat_category",
            ),
            models.CheckConstraint(
                condition=Q(quantity__gte=1) & Q(quantity__lte=6),
                name="cart_line_quantity_between_1_and_6",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.quantity} x {self.seat_category}"

    @property
    def line_total(self) -> Decimal:
        return self.seat_category.price * self.quantity
