import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_homepage_is_available(client):
    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "Bienvenue sur la billetterie de concerts" in response.content.decode()
