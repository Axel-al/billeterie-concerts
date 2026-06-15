from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from concerts.models import Concert, SeatCategory


class OrderStatus(models.TextChoices):
    PENDING = "pending", "En attente de paiement"
    PAID = "paid", "Payée"
    REFUSED = "refused", "Refusée"
    CANCELLED = "cancelled", "Annulée"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="utilisateur",
    )
    concert = models.ForeignKey(
        Concert,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="concert",
    )
    status = models.CharField(
        "statut",
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    total_amount = models.DecimalField(
        "montant total",
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    created_at = models.DateTimeField("date de création", auto_now_add=True)
    updated_at = models.DateTimeField("date de mise à jour", auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Commande #{self.pk} - {self.user}"

    @property
    def total_quantity(self) -> int:
        return sum(line.quantity for line in self.lines.all())

    @property
    def is_final(self) -> bool:
        return self.status == OrderStatus.PAID


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="lines",
        verbose_name="commande",
    )
    seat_category = models.ForeignKey(
        SeatCategory,
        on_delete=models.PROTECT,
        related_name="order_lines",
        verbose_name="catégorie de place",
    )
    category_name_snapshot = models.CharField("catégorie achetée", max_length=120)
    unit_price = models.DecimalField("prix unitaire", max_digits=8, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(
        "quantité",
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    created_at = models.DateTimeField("date de création", auto_now_add=True)

    class Meta:
        ordering = ("id",)
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gte=1) & Q(quantity__lte=6),
                name="order_line_quantity_between_1_and_6",
            )
        ]

    def __str__(self) -> str:
        return f"{self.quantity} x {self.category_name_snapshot}"

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity
