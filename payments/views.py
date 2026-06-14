from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, FormView

from cart.services import validate_cart_for_checkout
from cart.views import active_cart_for_user, add_error_messages
from orders.models import Order, OrderStatus
from payments.forms import SimulatedPaymentForm
from payments.models import PaymentResult
from payments.services import process_simulated_card_payment


class SimulatedPaymentView(LoginRequiredMixin, FormView):
    template_name = "payments/payment_form.html"
    form_class = SimulatedPaymentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = active_cart_for_user(self.request.user)
        context["cart"] = cart

        if cart is None:
            context["payment_error"] = "Votre panier est vide."
            return context

        try:
            context["cart_validation"] = validate_cart_for_checkout(cart)
        except ValidationError as error:
            context["payment_error"] = " ".join(error.messages)

        return context

    def form_valid(self, form):
        cart = active_cart_for_user(self.request.user)
        if cart is None:
            messages.error(self.request, "Votre panier est vide.", extra_tags="danger")
            return redirect("cart:detail")

        try:
            payment = process_simulated_card_payment(
                cart,
                form.cleaned_data["card_number"],
            )
        except ValidationError as error:
            add_error_messages(self.request, error)
            return redirect("cart:checkout")

        if payment.result == PaymentResult.ACCEPTED:
            return redirect("payments:confirmation", pk=payment.order_id)
        return redirect("payments:refused", pk=payment.order_id)


class UserOrderMixin(LoginRequiredMixin):
    model = Order
    context_object_name = "order"

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user, status=self.order_status)
            .select_related("concert", "payment")
            .prefetch_related("lines")
        )


class PaymentConfirmationView(UserOrderMixin, DetailView):
    template_name = "payments/confirmation.html"
    order_status = OrderStatus.PAID


class RefusedPaymentView(UserOrderMixin, DetailView):
    template_name = "payments/refused.html"
    order_status = OrderStatus.REFUSED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["retry_payment_url"] = reverse("payments:simulate")
        return context
