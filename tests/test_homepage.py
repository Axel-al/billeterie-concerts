import pytest
from django.urls import resolve, reverse


@pytest.mark.django_db
def test_homepage_is_available(client):
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "Bienvenue sur la billetterie de concerts" in response.content.decode()


def test_homepage_url_name_resolves_to_root():
    assert reverse("home") == "/"
    assert resolve("/").url_name == "home"
