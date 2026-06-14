from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView

from cart.forms import AddTicketForm
from concerts.models import Concert, ConcertStatus
from concerts.services import (
    cancel_concert,
    close_concert_sales,
    sales_summaries_for_concerts,
)


def booking_unavailability_reason(concert):
    if concert.status == ConcertStatus.CANCELLED:
        return "Ce concert est annulé. Aucune réservation n’est possible."
    if concert.status == ConcertStatus.CLOSED:
        return (
            "Les ventes de ce concert sont clôturées. "
            "Aucune réservation n’est possible."
        )
    if concert.is_past():
        return "Ce concert est déjà passé. Aucune réservation n’est possible."
    if (
        concert.status == ConcertStatus.SOLD_OUT
        or not concert.has_available_stock()
    ):
        return "Ce concert est complet. Il ne reste aucune place disponible."
    if concert.status != ConcertStatus.OPEN:
        return "Ce concert n’est pas ouvert à la vente."
    return ""


class ConcertListView(ListView):
    template_name = "concerts/concert_list.html"
    context_object_name = "concerts"

    def get_queryset(self):
        return (
            Concert.objects.filter(
                status=ConcertStatus.OPEN,
                starts_at__gt=timezone.now(),
                seat_categories__stock_remaining__gt=0,
            )
            .distinct()
            .order_by("starts_at", "title")
        )


class ConcertDetailView(DetailView):
    template_name = "concerts/concert_detail.html"
    context_object_name = "concert"
    queryset = Concert.objects.exclude(status=ConcertStatus.DRAFT).prefetch_related(
        "seat_categories"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_bookable = self.object.is_bookable()
        context["is_bookable"] = is_bookable
        context["booking_unavailability_reason"] = (
            booking_unavailability_reason(self.object)
        )
        if is_bookable and self.request.user.is_authenticated:
            context["add_ticket_form"] = AddTicketForm(self.object)
        return context


class AdminPermissionRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    raise_exception = True

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )


class ConcertSalesOverviewView(AdminPermissionRequiredMixin, ListView):
    template_name = "concerts/admin_sales_overview.html"
    context_object_name = "concerts"
    permission_required = ("concerts.view_concert", "orders.view_order")

    def get_queryset(self):
        return Concert.objects.prefetch_related("seat_categories").order_by(
            "starts_at",
            "title",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sales_summaries"] = sales_summaries_for_concerts(
            context["concerts"],
        )
        return context


class ConcertAdminActionView(AdminPermissionRequiredMixin, View):
    permission_required = ("concerts.change_concert",)
    success_message = ""

    def update_concert(self, concert):
        raise NotImplementedError

    def post(self, request, pk):
        concert = get_object_or_404(Concert, pk=pk)
        self.update_concert(concert)
        messages.success(request, self.success_message.format(concert=concert))
        return redirect("concerts:admin_sales_overview")


class CancelConcertView(ConcertAdminActionView):
    success_message = "Le concert « {concert.title} » a été annulé."

    def update_concert(self, concert):
        return cancel_concert(concert)


class CloseConcertSalesView(ConcertAdminActionView):
    success_message = "Les ventes du concert « {concert.title} » ont été clôturées."

    def update_concert(self, concert):
        return close_concert_sales(concert)
