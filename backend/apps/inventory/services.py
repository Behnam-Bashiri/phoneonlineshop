from django.db import transaction

from apps.inventory.models import InventoryItem, StockMovement, Warehouse


class InventoryService:
    @staticmethod
    def get_default_warehouse():
        warehouse = Warehouse.objects.filter(is_default=True, is_active=True).first()
        if not warehouse:
            warehouse = Warehouse.objects.filter(is_active=True).first()
        return warehouse

    @staticmethod
    @transaction.atomic
    def adjust_stock(variant, warehouse, quantity, movement_type, performed_by=None, reference="", notes=""):
        item, _ = InventoryItem.objects.get_or_create(
            variant=variant,
            warehouse=warehouse,
            defaults={"quantity": 0},
        )

        if movement_type == StockMovement.MovementType.IN:
            item.quantity += quantity
        elif movement_type == StockMovement.MovementType.OUT:
            if item.available < quantity:
                raise ValueError("Insufficient inventory.")
            item.quantity -= quantity
        elif movement_type == StockMovement.MovementType.ADJUSTMENT:
            item.quantity = quantity
        elif movement_type == StockMovement.MovementType.RETURN:
            item.quantity += quantity

        item.save(update_fields=["quantity", "updated_at"])

        variant.stock_quantity = sum(
            inv.quantity for inv in variant.inventory.all()
        )
        variant.save(update_fields=["stock_quantity"])

        StockMovement.objects.create(
            variant=variant,
            warehouse=warehouse,
            movement_type=movement_type,
            quantity=quantity,
            reference=reference,
            notes=notes,
            performed_by=performed_by,
        )
        return item

    @staticmethod
    def reserve_stock(variant, quantity):
        warehouse = InventoryService.get_default_warehouse()
        if not warehouse:
            if variant.available_stock < quantity:
                raise ValueError("Insufficient stock.")
            variant.reserved_quantity += quantity
            variant.save(update_fields=["reserved_quantity"])
            return

        item = InventoryItem.objects.filter(variant=variant, warehouse=warehouse).first()
        if not item or item.available < quantity:
            raise ValueError("Insufficient inventory.")
        item.reserved += quantity
        item.save(update_fields=["reserved", "updated_at"])
        variant.reserved_quantity += quantity
        variant.save(update_fields=["reserved_quantity"])

    @staticmethod
    def release_stock(variant, quantity):
        warehouse = InventoryService.get_default_warehouse()
        if warehouse:
            item = InventoryItem.objects.filter(variant=variant, warehouse=warehouse).first()
            if item:
                item.reserved = max(0, item.reserved - quantity)
                item.save(update_fields=["reserved", "updated_at"])
        variant.reserved_quantity = max(0, variant.reserved_quantity - quantity)
        variant.save(update_fields=["reserved_quantity"])
