from django.urls import path

from concerts.views import (
    CancelConcertView,
    CloseConcertSalesView,
    ConcertDetailView,
    ConcertListView,
    ConcertSalesOverviewView,
)

app_name = "concerts"

urlpatterns = [
    path("", ConcertListView.as_view(), name="list"),
    path(
        "administration/ventes/",
        ConcertSalesOverviewView.as_view(),
        name="admin_sales_overview",
    ),
    path(
        "administration/concerts/<int:pk>/annuler/",
        CancelConcertView.as_view(),
        name="admin_cancel",
    ),
    path(
        "administration/concerts/<int:pk>/cloturer/",
        CloseConcertSalesView.as_view(),
        name="admin_close",
    ),
    path("<int:pk>/", ConcertDetailView.as_view(), name="detail"),
]
