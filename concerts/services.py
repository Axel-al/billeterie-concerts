from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import Coalesce

from concerts.models import Concert, ConcertStatus
from orders.models import Order, OrderLine, OrderStatus


@dataclass(frozen=True)
class ConcertSalesSummary:
    concert: Concert
    paid_orders_count: int
    tickets_sold: int
    revenue: Decimal
    stock_initial: int
    stock_remaining: int


def cancel_concert(concert: Concert) -> Concert:
    concert.status = ConcertStatus.CANCELLED
    concert.save(update_fields=("status", "updated_at"))
    return concert


def close_concert_sales(concert: Concert) -> Concert:
    concert.status = ConcertStatus.CLOSED
    concert.save(update_fields=("status", "updated_at"))
    return concert


def sales_summary_for_concert(concert: Concert) -> ConcertSalesSummary:
    paid_orders = Order.objects.filter(concert=concert, status=OrderStatus.PAID)
    paid_order_stats = paid_orders.aggregate(
        revenue=Coalesce(Sum("total_amount"), Decimal("0.00")),
    )
    paid_ticket_stats = OrderLine.objects.filter(
        order__concert=concert,
        order__status=OrderStatus.PAID,
    ).aggregate(
        tickets_sold=Coalesce(Sum("quantity"), 0),
    )
    stock_stats = concert.seat_categories.aggregate(
        stock_initial=Coalesce(Sum("stock_initial"), 0),
        stock_remaining=Coalesce(Sum("stock_remaining"), 0),
    )

    return ConcertSalesSummary(
        concert=concert,
        paid_orders_count=paid_orders.count(),
        tickets_sold=paid_ticket_stats["tickets_sold"],
        revenue=paid_order_stats["revenue"],
        stock_initial=stock_stats["stock_initial"],
        stock_remaining=stock_stats["stock_remaining"],
    )


def sales_summaries_for_concerts(concerts) -> list[ConcertSalesSummary]:
    return [sales_summary_for_concert(concert) for concert in concerts]
