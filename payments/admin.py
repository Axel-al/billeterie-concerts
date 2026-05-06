from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "result", "processed_at")
    list_filter = ("result", "processed_at")
    search_fields = ("order__user__email", "order__concert__title")
    autocomplete_fields = ("order",)
