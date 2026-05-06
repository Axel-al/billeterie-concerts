from django.db import models

from orders.models import Order


class PaymentResult(models.TextChoices):
    ACCEPTED = "accepted", "Accepte"
    REFUSED = "refused", "Refuse"


class Payment(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name="commande",
    )
    amount = models.DecimalField("montant", max_digits=10, decimal_places=2)
    result = models.CharField(
        "resultat",
        max_length=20,
        choices=PaymentResult.choices,
    )
    processed_at = models.DateTimeField("date de paiement", auto_now_add=True)

    class Meta:
        ordering = ("-processed_at",)

    def __str__(self) -> str:
        return f"Paiement #{self.pk} - {self.get_result_display()}"
