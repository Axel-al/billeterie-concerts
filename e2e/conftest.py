import os
from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal

# pytest-playwright can keep an event loop active during Django test DB setup.
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from concerts.models import Concert, ConcertStatus, SeatCategory

E2E_PASSWORD = "MotDePasseTresSolide2026!"


@dataclass(frozen=True)
class BookingScenario:
    user: object
    password: str
    concert: Concert
    category: SeatCategory


@pytest.fixture
def booking_scenario(transactional_db):
    user = get_user_model().objects.create_user(
        email="client.e2e@example.com",
        password=E2E_PASSWORD,
        first_name="Client",
        last_name="E2E",
    )
    concert = Concert.objects.create(
        title="Nuit Playwright",
        artist="The Stable Selectors",
        description="Un concert de validation end-to-end.",
        starts_at=timezone.now() + timedelta(days=30),
        venue="Salle Test",
        status=ConcertStatus.OPEN,
    )
    category = SeatCategory.objects.create(
        concert=concert,
        name="Fosse",
        price=Decimal("40.00"),
        stock_initial=8,
        stock_remaining=8,
    )
    SeatCategory.objects.create(
        concert=concert,
        name="Balcon",
        price=Decimal("55.00"),
        stock_initial=4,
        stock_remaining=4,
    )
    return BookingScenario(
        user=user,
        password=E2E_PASSWORD,
        concert=concert,
        category=category,
    )
