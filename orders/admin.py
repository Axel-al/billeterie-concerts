from django.contrib import admin

from orders.models import Order, OrderLine


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    autocomplete_fields = ("seat_category",)
    readonly_fields = ("category_name_snapshot", "unit_price", "quantity")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "concert",
        "status",
        "total_amount",
        "total_quantity",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "concert__title", "concert__artist")
    autocomplete_fields = ("user", "concert")
    inlines = (OrderLineInline,)


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "category_name_snapshot",
        "quantity",
        "unit_price",
    )
    list_filter = ("order__status",)
    search_fields = (
        "order__user__email",
        "order__concert__title",
        "category_name_snapshot",
    )
    autocomplete_fields = ("order", "seat_category")
