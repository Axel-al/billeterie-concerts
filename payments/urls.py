from django.urls import path

from payments.views import (
    PaymentConfirmationView,
    RefusedPaymentView,
    SimulatedPaymentView,
)

app_name = "payments"

urlpatterns = [
    path("", SimulatedPaymentView.as_view(), name="simulate"),
    path(
        "confirmation/<int:pk>/",
        PaymentConfirmationView.as_view(),
        name="confirmation",
    ),
    path("refus/<int:pk>/", RefusedPaymentView.as_view(), name="refused"),
]
