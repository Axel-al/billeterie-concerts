from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "result", "processed_at")
    list_filter = ("result", "processed_at")
    search_fields = ("order__user__email", "order__concert__title")
    readonly_fields = ("order", "amount", "result", "processed_at")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
