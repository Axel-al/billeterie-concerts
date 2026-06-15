from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

admin.site.site_header = "Administration de la billetterie"
admin.site.site_title = "Administration de la billetterie"
admin.site.index_title = "Gestion de la billetterie"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("", include("accounts.urls")),
    path("commandes/", include("orders.urls")),
    path("panier/", include("cart.urls")),
    path("paiement/", include("payments.urls")),
    path("concerts/", include("concerts.urls")),
    path("admin/", admin.site.urls),
]
