from django.contrib import admin

from orders.models import Order, OrderLine


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    readonly_fields = (
        "seat_category",
        "category_name_snapshot",
        "unit_price",
        "quantity",
        "created_at",
    )
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


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
    readonly_fields = (
        "user",
        "concert",
        "status",
        "total_amount",
        "total_quantity",
        "created_at",
        "updated_at",
    )
    inlines = (OrderLineInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


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
    readonly_fields = (
        "order",
        "seat_category",
        "category_name_snapshot",
        "unit_price",
        "quantity",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
