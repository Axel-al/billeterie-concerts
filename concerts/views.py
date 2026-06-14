from django.utils import timezone
from django.views.generic import DetailView, ListView

from cart.forms import AddTicketForm
from concerts.models import Concert, ConcertStatus


def booking_unavailability_reason(concert):
    if concert.status == ConcertStatus.CANCELLED:
        return "Ce concert est annulé. Aucune réservation n’est possible."
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
