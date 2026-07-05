from django.contrib import admin

from apps.payments.models import Payment, PaymentLog


class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0
    readonly_fields = ["event", "data", "ip_address", "created_at"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "user", "amount", "method", "status", "gateway", "paid_at"]
    list_filter = ["status", "method", "gateway"]
    search_fields = ["transaction_id", "order__order_number", "user__email"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [PaymentLogInline]


@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ["payment", "event", "ip_address", "created_at"]
    list_filter = ["event"]
    search_fields = ["payment__transaction_id"]
