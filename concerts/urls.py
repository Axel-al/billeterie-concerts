from django.urls import path

from concerts.views import ConcertDetailView, ConcertListView

app_name = "concerts"

urlpatterns = [
    path("", ConcertListView.as_view(), name="list"),
    path("<int:pk>/", ConcertDetailView.as_view(), name="detail"),
]
