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
from orders.models import Order, OrderLine, OrderStatus
from payments.models import Payment, PaymentResult

E2E_PASSWORD = "MotDePasseTresSolide2026!"


@dataclass(frozen=True)
class BookingScenario:
    user: object
    password: str
    concert: Concert
    category: SeatCategory


@dataclass(frozen=True)
class PerformanceScenario:
    user: object
    concert: Concert
    category: SeatCategory
    order: Order


def _create_e2e_user(email: str):
    return get_user_model().objects.create_user(
        email=email,
        password=E2E_PASSWORD,
        first_name="Client",
        last_name="E2E",
    )


def _create_e2e_concert(title: str) -> tuple[Concert, SeatCategory]:
    concert = Concert.objects.create(
        title=title,
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
    return concert, category


@pytest.fixture
def booking_scenario(transactional_db):
    user = _create_e2e_user("client.e2e@example.com")
    concert, category = _create_e2e_concert("Nuit Playwright")
    return BookingScenario(
        user=user,
        password=E2E_PASSWORD,
        concert=concert,
        category=category,
    )


@pytest.fixture
def performance_scenario(transactional_db):
    user = _create_e2e_user("performance.e2e@example.com")
    concert, category = _create_e2e_concert("Nuit Performance")
    order = Order.objects.create(
        user=user,
        concert=concert,
        status=OrderStatus.PAID,
        total_amount=Decimal("80.00"),
    )
    OrderLine.objects.create(
        order=order,
        seat_category=category,
        category_name_snapshot=category.name,
        unit_price=category.price,
        quantity=2,
    )
    Payment.objects.create(
        order=order,
        amount=order.total_amount,
        result=PaymentResult.ACCEPTED,
    )
    return PerformanceScenario(
        user=user,
        concert=concert,
        category=category,
        order=order,
    )
