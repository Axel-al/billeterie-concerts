from django.contrib import admin

from concerts.models import Concert, SeatCategory


class SeatCategoryInline(admin.TabularInline):
    model = SeatCategory
    extra = 0


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "artist",
        "starts_at",
        "venue",
        "status",
        "has_available_stock",
    )
    list_filter = ("status", "starts_at")
    search_fields = ("title", "artist", "venue")
    inlines = (SeatCategoryInline,)


@admin.register(SeatCategory)
class SeatCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "concert",
        "price",
        "stock_initial",
        "stock_remaining",
    )
    list_filter = ("concert__status",)
    search_fields = ("name", "concert__title", "concert__artist")
    autocomplete_fields = ("concert",)
