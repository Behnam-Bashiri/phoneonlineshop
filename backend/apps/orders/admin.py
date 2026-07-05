from django.contrib import admin

from apps.orders.models import City, Invoice, Order, OrderItem, OrderStatusHistory, Province, ShippingMethod


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product_name", "variant_sku", "total_price"]


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ["status", "note", "changed_by", "created_at"]


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name", "name_fa", "code", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "name_fa", "code"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "name_fa", "province", "is_active"]
    list_filter = ["province", "is_active"]
    search_fields = ["name", "name_fa"]


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ["name", "base_cost", "estimated_days_min", "estimated_days_max", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "name_fa"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "status", "total", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["order_number", "user__email", "tracking_number", "guest_email"]
    readonly_fields = ["order_number", "created_at", "updated_at"]
    inlines = [OrderItemInline, OrderStatusHistoryInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "order", "issued_at"]
    search_fields = ["invoice_number", "order__order_number"]
