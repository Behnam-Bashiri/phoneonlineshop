from django.contrib import admin

from apps.inventory.models import InventoryItem, StockMovement, Supplier, Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "is_active", "is_default"]
    list_filter = ["is_active", "is_default"]
    search_fields = ["name", "code"]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["name", "contact_person", "email", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "email"]


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ["variant", "warehouse", "quantity", "reserved", "reorder_level"]
    list_filter = ["warehouse"]
    search_fields = ["variant__sku", "variant__product__name"]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ["variant", "warehouse", "movement_type", "quantity", "performed_by", "created_at"]
    list_filter = ["movement_type", "warehouse"]
    search_fields = ["variant__sku", "reference"]
