import pytest
from django.contrib.auth import authenticate, get_user_model
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
    assert str(user) == "client@example.com"


@pytest.mark.django_db
def test_user_manager_normalizes_email_domain():
    user = get_user_model().objects.create_user(
        email="Client@EXAMPLE.COM",
        password="mot-de-passe-solide",
    )

    assert user.email == "Client@example.com"


@pytest.mark.django_db
def test_user_manager_requires_email():
    with pytest.raises(ValueError, match="adresse email"):
        get_user_model().objects.create_user(email="", password="mot-de-passe-solide")


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


@pytest.mark.django_db
def test_user_can_authenticate_with_email():
    password = "mot-de-passe-solide"
    get_user_model().objects.create_user(
        email="client@example.com",
        password=password,
    )

    user = authenticate(email="client@example.com", password=password)

    assert user is not None
    assert user.email == "client@example.com"


@pytest.mark.django_db
def test_superuser_defaults_to_staff_and_superuser_flags():
    superuser = get_user_model().objects.create_superuser(
        email="admin@example.com",
        password="mot-de-passe-solide",
    )

    assert superuser.is_staff
    assert superuser.is_superuser


@pytest.mark.django_db
def test_superuser_requires_staff_flag():
    with pytest.raises(ValueError, match="is_staff=True"):
        get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="mot-de-passe-solide",
            is_staff=False,
        )


@pytest.mark.django_db
def test_superuser_requires_superuser_flag():
    with pytest.raises(ValueError, match="is_superuser=True"):
        get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="mot-de-passe-solide",
            is_superuser=False,
        )
