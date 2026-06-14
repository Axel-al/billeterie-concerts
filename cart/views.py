from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from cart.forms import AddTicketForm
from cart.models import Cart, CartStatus
from cart.services import add_ticket_to_cart, validate_cart_for_checkout
from concerts.models import Concert, ConcertStatus


def active_cart_for_user(user):
    return (
        Cart.objects.filter(user=user, status=CartStatus.ACTIVE)
        .select_related("concert")
        .prefetch_related("lines__seat_category")
        .first()
    )


def add_error_messages(request, error):
    for message in getattr(error, "messages", [str(error)]):
        messages.error(request, message, extra_tags="danger")


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = active_cart_for_user(self.request.user)
        return context


class AddTicketToCartView(LoginRequiredMixin, View):
    def post(self, request, concert_pk):
        concert = get_object_or_404(
            Concert.objects.exclude(status=ConcertStatus.DRAFT),
            pk=concert_pk,
        )
        form = AddTicketForm(concert, request.POST)
        detail_url = reverse("concerts:detail", args=[concert.pk])

        if not form.is_valid():
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error, extra_tags="danger")
            return redirect(detail_url)

        try:
            add_ticket_to_cart(
                request.user,
                form.cleaned_data["seat_category"],
                form.cleaned_data["quantity"],
            )
        except ValidationError as error:
            add_error_messages(request, error)
            return redirect(detail_url)

        messages.success(request, "Les billets ont été ajoutés au panier.")
        return redirect("cart:detail")


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = "cart/checkout.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = active_cart_for_user(self.request.user)
        context["cart"] = cart

        if cart is None:
            context["checkout_error"] = "Votre panier est vide."
            return context

        try:
            context["cart_validation"] = validate_cart_for_checkout(cart)
        except ValidationError as error:
            context["checkout_error"] = " ".join(error.messages)

        return context
