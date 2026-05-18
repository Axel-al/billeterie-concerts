import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

VALID_PASSWORD = "MotDePasseTresSolide2026!"


def registration_data(email="client@example.com", password=VALID_PASSWORD):
    return {
        "first_name": "Camille",
        "last_name": "Martin",
        "email": email,
        "password1": password,
        "password2": password,
    }


def test_authentication_pages_use_french_labels(client):
    signup_response = client.get(reverse("accounts:signup"))
    login_response = client.get(reverse("accounts:login"))

    signup_content = signup_response.content.decode()
    login_content = login_response.content.decode()
    assert signup_response.status_code == 200
    assert login_response.status_code == 200
    assert "Adresse email" in signup_content
    assert "Prénom" in signup_content
    assert "Mot de passe" in signup_content
    assert "Créer mon compte" in signup_content
    assert "Adresse email" in login_content
    assert "Mot de passe" in login_content
    assert "Se connecter" in login_content


@pytest.mark.django_db
def test_account_creation_succeeds_with_unique_email(client):
    response = client.post(
        reverse("accounts:signup"),
        data=registration_data(),
    )

    user = get_user_model().objects.get(email="client@example.com")
    assert response.status_code == 302
    assert response["Location"] == reverse("accounts:personal_area")
    assert client.session["_auth_user_id"] == str(user.pk)


@pytest.mark.django_db
def test_duplicate_email_registration_is_rejected_with_french_message(client):
    user_model = get_user_model()
    user_model.objects.create_user(
        email="client@example.com",
        password=VALID_PASSWORD,
    )

    response = client.post(
        reverse("accounts:signup"),
        data=registration_data(email="CLIENT@example.com"),
    )

    assert response.status_code == 200
    assert user_model.objects.count() == 1
    assert (
        "Un compte existe déjà avec cette adresse email."
        in response.content.decode()
    )


@pytest.mark.django_db
def test_registered_password_is_not_stored_in_plain_text(client):
    client.post(
        reverse("accounts:signup"),
        data=registration_data(password=VALID_PASSWORD),
    )

    user = get_user_model().objects.get(email="client@example.com")
    assert user.password != VALID_PASSWORD
    assert user.check_password(VALID_PASSWORD)


@pytest.mark.django_db
def test_login_succeeds_with_valid_credentials(client):
    get_user_model().objects.create_user(
        email="client@example.com",
        password=VALID_PASSWORD,
    )

    response = client.post(
        reverse("accounts:login"),
        data={"username": "client@example.com", "password": VALID_PASSWORD},
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("accounts:personal_area")
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_login_fails_with_invalid_credentials(client):
    get_user_model().objects.create_user(
        email="client@example.com",
        password=VALID_PASSWORD,
    )

    response = client.post(
        reverse("accounts:login"),
        data={"username": "client@example.com", "password": "mauvais-secret"},
    )

    assert response.status_code == 200
    assert "_auth_user_id" not in client.session
    assert "Adresse email ou mot de passe invalide." in response.content.decode()


@pytest.mark.django_db
def test_logout_clears_session_through_post_logout_view(client):
    user = get_user_model().objects.create_user(
        email="client@example.com",
        password=VALID_PASSWORD,
    )
    client.force_login(user)

    response = client.post(reverse("accounts:logout"))

    assert response.status_code == 302
    assert response["Location"] == reverse("home")
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_personal_area_requires_authentication(client):
    response = client.get(reverse("accounts:personal_area"))

    expected_url = (
        f"{reverse('accounts:login')}?next={reverse('accounts:personal_area')}"
    )
    assert response.status_code == 302
    assert response["Location"] == expected_url


@pytest.mark.django_db
def test_authenticated_user_can_access_personal_area(client):
    user = get_user_model().objects.create_user(
        email="client@example.com",
        first_name="Camille",
        password=VALID_PASSWORD,
    )
    client.force_login(user)

    response = client.get(reverse("accounts:personal_area"))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Mon espace" in content
    assert "client@example.com" in content
    assert "Bienvenue, Camille." in content


@pytest.mark.django_db
def test_registered_standard_user_has_no_admin_privileges(client):
    client.post(
        reverse("accounts:signup"),
        data=registration_data(),
    )

    user = get_user_model().objects.get(email="client@example.com")
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_navigation_uses_post_logout_form_for_authenticated_user(client):
    user = get_user_model().objects.create_user(
        email="client@example.com",
        password=VALID_PASSWORD,
    )
    client.force_login(user)

    response = client.get(reverse("home"))

    content = response.content.decode()
    assert 'method="post" action="/deconnexion/"' in content
    assert "Déconnexion" in content
    assert "Mon espace" in content
