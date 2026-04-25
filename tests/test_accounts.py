import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError


@pytest.mark.django_db
def test_user_uses_email_as_identifier():
    user = get_user_model().objects.create_user(
        email="client@example.com",
        password="mot-de-passe-solide",
    )

    assert user.email == "client@example.com"
    assert user.username is None
    assert user.get_username() == "client@example.com"


@pytest.mark.django_db
def test_user_email_must_be_unique():
    user_model = get_user_model()
    user_model.objects.create_user(
        email="client@example.com",
        password="mot-de-passe-solide",
    )

    with pytest.raises(IntegrityError):
        user_model.objects.create_user(
            email="client@example.com",
            password="autre-mot-de-passe",
        )


@pytest.mark.django_db
def test_user_password_is_hashed():
    password = "mot-de-passe-solide"
    user = get_user_model().objects.create_user(
        email="client@example.com",
        password=password,
    )

    assert user.password != password
    assert user.check_password(password)
