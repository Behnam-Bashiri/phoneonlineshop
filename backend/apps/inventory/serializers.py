from rest_framework import serializers

from apps.catalog.serializers import ProductVariantSerializer
from apps.inventory.models import InventoryItem, StockMovement, Supplier, Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "code", "address", "is_active", "is_default"]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "contact_person", "email", "phone", "address", "is_active"]


class InventoryItemSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    available = serializers.IntegerField(read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            "id",
            "variant",
            "warehouse",
            "quantity",
            "reserved",
            "available",
            "reorder_level",
            "supplier",
        ]


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            "id",
            "variant",
            "warehouse",
            "movement_type",
            "quantity",
            "reference",
            "notes",
            "performed_by",
            "created_at",
        ]
        read_only_fields = fields
