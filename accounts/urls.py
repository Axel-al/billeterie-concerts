from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import LoginView, PersonalAreaView, SignUpView

app_name = "accounts"

urlpatterns = [
    path("inscription/", SignUpView.as_view(), name="signup"),
    path("connexion/", LoginView.as_view(), name="login"),
    path("deconnexion/", LogoutView.as_view(), name="logout"),
    path("mon-espace/", PersonalAreaView.as_view(), name="personal_area"),
]
