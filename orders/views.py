from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from orders.models import Order, OrderStatus


def paid_orders_for_user(user):
    return (
        Order.objects.filter(user=user, status=OrderStatus.PAID)
        .select_related("concert")
        .prefetch_related("lines")
    )


class OrderListView(LoginRequiredMixin, ListView):
    template_name = "orders/list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return paid_orders_for_user(self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "orders/detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return paid_orders_for_user(self.request.user)
