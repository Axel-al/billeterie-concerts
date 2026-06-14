from django.contrib import admin, messages

from concerts.models import Concert, SeatCategory
from concerts.services import (
    cancel_concert,
    close_concert_sales,
    sales_summary_for_concert,
)


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
        "total_stock_initial",
        "total_stock_remaining",
        "paid_orders_count",
        "paid_tickets_sold",
        "paid_revenue",
    )
    list_filter = ("status", "starts_at")
    search_fields = ("title", "artist", "venue")
    inlines = (SeatCategoryInline,)
    actions = ("cancel_selected_concerts", "close_selected_concerts")

    @admin.display(description="stock initial")
    def total_stock_initial(self, obj):
        return sales_summary_for_concert(obj).stock_initial

    @admin.display(description="stock restant")
    def total_stock_remaining(self, obj):
        return sales_summary_for_concert(obj).stock_remaining

    @admin.display(description="commandes payees")
    def paid_orders_count(self, obj):
        return sales_summary_for_concert(obj).paid_orders_count

    @admin.display(description="billets vendus")
    def paid_tickets_sold(self, obj):
        return sales_summary_for_concert(obj).tickets_sold

    @admin.display(description="revenu paye")
    def paid_revenue(self, obj):
        return sales_summary_for_concert(obj).revenue

    @admin.action(description="Annuler les concerts selectionnes")
    def cancel_selected_concerts(self, request, queryset):
        updated_count = 0
        for concert in queryset:
            cancel_concert(concert)
            updated_count += 1
        self.message_user(
            request,
            f"{updated_count} concert(s) annule(s).",
            level=messages.SUCCESS,
        )

    @admin.action(description="Cloturer les ventes des concerts selectionnes")
    def close_selected_concerts(self, request, queryset):
        updated_count = 0
        for concert in queryset:
            close_concert_sales(concert)
            updated_count += 1
        self.message_user(
            request,
            f"Ventes cloturees pour {updated_count} concert(s).",
            level=messages.SUCCESS,
        )


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
