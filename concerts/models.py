from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone


class ConcertStatus(models.TextChoices):
    DRAFT = "draft", "Brouillon"
    OPEN = "open", "Ouvert a la vente"
    SOLD_OUT = "sold_out", "Complet"
    CANCELLED = "cancelled", "Annule"
    FINISHED = "finished", "Termine"


class Concert(models.Model):
    title = models.CharField("titre", max_length=200)
    artist = models.CharField("artiste ou groupe", max_length=200)
    description = models.TextField("description", blank=True)
    starts_at = models.DateTimeField("date et heure")
    venue = models.CharField("lieu", max_length=200)
    status = models.CharField(
        "statut",
        max_length=20,
        choices=ConcertStatus.choices,
        default=ConcertStatus.DRAFT,
    )
    created_at = models.DateTimeField("date de creation", auto_now_add=True)
    updated_at = models.DateTimeField("date de mise a jour", auto_now=True)

    class Meta:
        ordering = ("starts_at", "title")

    def __str__(self) -> str:
        return f"{self.title} - {self.artist}"

    def is_past(self, now=None) -> bool:
        current_time = now or timezone.now()
        return self.starts_at <= current_time

    def has_available_stock(self) -> bool:
        if self.pk is None:
            return False
        return self.seat_categories.filter(stock_remaining__gt=0).exists()

    def is_bookable(self, now=None) -> bool:
        return (
            self.status == ConcertStatus.OPEN
            and not self.is_past(now)
            and self.has_available_stock()
        )


class SeatCategory(models.Model):
    concert = models.ForeignKey(
        Concert,
        on_delete=models.CASCADE,
        related_name="seat_categories",
        verbose_name="concert",
    )
    name = models.CharField("nom", max_length=120)
    price = models.DecimalField(
        "prix",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    stock_initial = models.PositiveIntegerField("stock initial")
    stock_remaining = models.PositiveIntegerField("stock restant")
    created_at = models.DateTimeField("date de creation", auto_now_add=True)
    updated_at = models.DateTimeField("date de mise a jour", auto_now=True)

    class Meta:
        ordering = ("concert", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("concert", "name"),
                name="unique_seat_category_name_per_concert",
            ),
            models.CheckConstraint(
                condition=Q(stock_initial__gte=0),
                name="seat_category_stock_initial_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(stock_remaining__gte=0),
                name="seat_category_stock_remaining_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.concert.title} - {self.name}"

    def has_stock_for(self, quantity: int) -> bool:
        return self.stock_remaining >= quantity
