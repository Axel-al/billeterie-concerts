from django.urls import path

from cart.views import AddTicketToCartView, CartDetailView, CheckoutView

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="detail"),
    path("ajouter/<int:concert_pk>/", AddTicketToCartView.as_view(), name="add_ticket"),
    path("validation/", CheckoutView.as_view(), name="checkout"),
]
