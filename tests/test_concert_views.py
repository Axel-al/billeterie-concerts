from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from concerts.models import Concert, ConcertStatus, SeatCategory


@pytest.fixture(autouse=True)
def frozen_clock():
    with freeze_time("2026-06-14 12:00:00"):
        yield


def create_concert(
    *,
    title="Nuit Electrique",
    artist="The Validation Keys",
    status=ConcertStatus.OPEN,
    starts_at=None,
):
    return Concert.objects.create(
        title=title,
        artist=artist,
        description="Une soirée de concert à découvrir.",
        starts_at=starts_at or timezone.now() + timedelta(days=30),
        venue="Le Grand Dôme",
        status=status,
    )


def create_category(
    concert,
    *,
    name="Fosse",
    price=Decimal("35.00"),
    stock=10,
):
    return SeatCategory.objects.create(
        concert=concert,
        name=name,
        price=price,
        stock_initial=stock,
        stock_remaining=stock,
    )


@pytest.mark.django_db
def test_concert_list_returns_200_and_only_displays_bookable_concerts(client):
    visible = create_concert()
    create_category(visible)

    cancelled = create_concert(
        title="Concert annule",
        status=ConcertStatus.CANCELLED,
    )
    create_category(cancelled)

    closed = create_concert(
        title="Concert cloture",
        status=ConcertStatus.CLOSED,
    )
    create_category(closed)

    past = create_concert(
        title="Concert passe",
        starts_at=timezone.now() - timedelta(days=1),
    )
    create_category(past)

    stockless = create_concert(title="Concert sans stock")
    create_category(stockless, stock=0)

    draft = create_concert(
        title="Concert brouillon",
        status=ConcertStatus.DRAFT,
    )
    create_category(draft)

    response = client.get(reverse("concerts:list"))

    content = response.content.decode()
    assert response.status_code == 200
    assert visible.title in content
    assert visible.artist in content
    assert visible.venue in content
    assert cancelled.title not in content
    assert closed.title not in content
    assert past.title not in content
    assert stockless.title not in content
    assert draft.title not in content


@pytest.mark.django_db
def test_concert_list_displays_a_clear_empty_state(client):
    response = client.get(reverse("concerts:list"))

    assert response.status_code == 200
    assert (
        "Aucun concert n’est actuellement ouvert à la vente."
        in response.content.decode()
    )


@pytest.mark.django_db
def test_concert_detail_displays_required_information(client):
    concert = create_concert()
    create_category(
        concert,
        name="Balcon",
        price=Decimal("48.00"),
        stock=8,
    )
    create_category(
        concert,
        name="VIP",
        price=Decimal("95.00"),
        stock=0,
    )

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert concert.title in content
    assert concert.artist in content
    expected_date = timezone.localtime(concert.starts_at).strftime(
        "%d/%m/%Y à %H:%M"
    )
    assert expected_date in content
    assert concert.venue in content
    assert "Balcon" in content
    assert "48,00" in content
    assert ">8<" in content
    assert "VIP" in content
    assert "95,00" in content
    assert ">0<" in content


@pytest.mark.django_db
def test_bookable_concert_prompts_anonymous_visitor_to_log_in(client):
    concert = create_concert()
    create_category(concert)
    detail_url = reverse("concerts:detail", args=[concert.pk])

    response = client.get(detail_url)

    content = response.content.decode()
    login_url = reverse("accounts:login")
    assert response.status_code == 200
    assert "Ce concert est réservable" in content
    assert "Se connecter pour réserver" in content
    assert f'href="{login_url}?next={detail_url}"' in content


@pytest.mark.django_db
def test_bookable_concert_displays_add_to_cart_form_for_authenticated_user(client):
    concert = create_concert()
    create_category(concert)
    user = get_user_model().objects.create_user(
        email="client@example.com",
        password="mot-de-passe-solide",
    )
    client.force_login(user)

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Ajouter au panier" in content
    assert f'action="{reverse("cart:add_ticket", args=[concert.pk])}"' in content
    assert "Quantité" in content
    assert "Se connecter pour réserver" not in content


@pytest.mark.django_db
def test_cancelled_concert_detail_explains_unavailability_without_cta(client):
    concert = create_concert(status=ConcertStatus.CANCELLED)
    create_category(concert)

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Ce concert est annulé. Aucune réservation n’est possible." in content
    assert "Se connecter pour réserver" not in content


@pytest.mark.django_db
def test_closed_concert_detail_explains_unavailability_without_cta(client):
    concert = create_concert(status=ConcertStatus.CLOSED)
    create_category(concert)

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert (
        "Les ventes de ce concert sont clôturées. Aucune réservation n’est possible."
        in content
    )
    assert "Se connecter pour réserver" not in content


@pytest.mark.django_db
def test_past_concert_detail_explains_unavailability_without_cta(client):
    concert = create_concert(
        starts_at=timezone.now() - timedelta(minutes=1),
    )
    create_category(concert)

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert (
        "Ce concert est déjà passé. Aucune réservation n’est possible."
        in content
    )
    assert "Se connecter pour réserver" not in content


@pytest.mark.django_db
def test_stockless_concert_detail_explains_unavailability_without_cta(client):
    concert = create_concert()
    create_category(concert, stock=0)

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert (
        "Ce concert est complet. Il ne reste aucune place disponible." in content
    )
    assert "Se connecter pour réserver" not in content


@pytest.mark.django_db
def test_future_finished_concert_detail_explains_closed_sale_without_cta(client):
    concert = create_concert(status=ConcertStatus.FINISHED)
    create_category(concert)

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    content = response.content.decode()
    assert response.status_code == 200
    assert "Ce concert n’est pas ouvert à la vente." in content
    assert "Se connecter pour réserver" not in content


@pytest.mark.django_db
def test_draft_concert_detail_returns_404(client):
    concert = create_concert(status=ConcertStatus.DRAFT)
    create_category(concert)

    response = client.get(reverse("concerts:detail", args=[concert.pk]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_unknown_concert_detail_returns_404(client):
    response = client.get(reverse("concerts:detail", args=[999999]))

    assert response.status_code == 404
