import pytest
from django.urls import resolve, reverse


@pytest.mark.django_db
def test_homepage_is_available(client):
    response = client.get(reverse("home"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Bienvenue sur la billetterie de concerts" in content
    assert "Voir les concerts" in content
    assert f'href="{reverse("concerts:list")}"' in content
    assert ">Concerts</a>" in content


def test_homepage_url_name_resolves_to_root():
    assert reverse("home") == "/"
    assert resolve("/").url_name == "home"
