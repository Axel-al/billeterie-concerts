from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from concerts.models import Concert, ConcertStatus, SeatCategory


class Command(BaseCommand):
    help = "Cree un petit jeu de donnees de demonstration pour la billetterie."

    def handle(self, *args, **options):
        now = timezone.now()
        concerts = [
            {
                "title": "Nuit Electrique",
                "artist": "The Validation Keys",
                "description": "Concert ouvert a la vente pour les demonstrations.",
                "starts_at": now + timedelta(days=30),
                "venue": "Le Grand Dome",
                "status": ConcertStatus.OPEN,
                "categories": [
                    ("Fosse", Decimal("35.00"), 120, 120),
                    ("Balcon", Decimal("48.00"), 80, 80),
                    ("VIP", Decimal("95.00"), 20, 20),
                ],
            },
            {
                "title": "Silence Annule",
                "artist": "Muted Signals",
                "description": "Concert futur annule pour tester les refus.",
                "starts_at": now + timedelta(days=45),
                "venue": "Salle Horizon",
                "status": ConcertStatus.CANCELLED,
                "categories": [
                    ("Standard", Decimal("29.00"), 100, 100),
                    ("Premium", Decimal("59.00"), 30, 30),
                ],
            },
            {
                "title": "Hier Encore",
                "artist": "Legacy Band",
                "description": "Concert passe ou termine pour tester les refus.",
                "starts_at": now - timedelta(days=7),
                "venue": "Club Archive",
                "status": ConcertStatus.FINISHED,
                "categories": [
                    ("Assis", Decimal("25.00"), 60, 12),
                    ("Debout", Decimal("18.00"), 140, 0),
                ],
            },
        ]

        for concert_data in concerts:
            categories = concert_data.pop("categories")
            concert, _created = Concert.objects.update_or_create(
                title=concert_data["title"],
                artist=concert_data["artist"],
                defaults=concert_data,
            )
            for name, price, stock_initial, stock_remaining in categories:
                SeatCategory.objects.update_or_create(
                    concert=concert,
                    name=name,
                    defaults={
                        "price": price,
                        "stock_initial": stock_initial,
                        "stock_remaining": stock_remaining,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Jeu de donnees demo cree ou mis a jour."))
