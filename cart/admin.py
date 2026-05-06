from django.contrib import admin

from cart.models import Cart, CartLine


class CartLineInline(admin.TabularInline):
    model = CartLine
    extra = 0
    autocomplete_fields = ("seat_category",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "concert", "status", "total_quantity", "updated_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__email", "concert__title", "concert__artist")
    autocomplete_fields = ("user", "concert")
    inlines = (CartLineInline,)


@admin.register(CartLine)
class CartLineAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "seat_category", "quantity")
    list_filter = ("cart__status",)
    search_fields = (
        "cart__user__email",
        "seat_category__name",
        "seat_category__concert__title",
    )
    autocomplete_fields = ("cart", "seat_category")
