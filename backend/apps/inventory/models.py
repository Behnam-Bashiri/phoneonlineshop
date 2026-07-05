from django.db import models

from core.models import TimeStampedModel


class Warehouse(TimeStampedModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "warehouses"
        verbose_name_plural = "warehouses"

    def __str__(self):
        return self.name


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "suppliers"

    def __str__(self):
        return self.name


class InventoryItem(TimeStampedModel):
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.CASCADE, related_name="inventory")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "inventory_items"
        unique_together = ["variant", "warehouse"]

    @property
    def available(self):
        return max(0, self.quantity - self.reserved)


class StockMovement(TimeStampedModel):
    class MovementType(models.TextChoices):
        IN = "in", "Stock In"
        OUT = "out", "Stock Out"
        ADJUSTMENT = "adjustment", "Adjustment"
        RETURN = "return", "Return"
        TRANSFER = "transfer", "Transfer"

    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.CASCADE, related_name="stock_movements")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    performed_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "stock_movements"
        ordering = ["-created_at"]
