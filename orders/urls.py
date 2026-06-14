from django.urls import path

from orders.views import OrderDetailView, OrderListView

app_name = "orders"

urlpatterns = [
    path("", OrderListView.as_view(), name="list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="detail"),
]
