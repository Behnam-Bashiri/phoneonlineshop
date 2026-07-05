import uuid

from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Province(TimeStampedModel):
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "provinces"
        verbose_name_plural = "provinces"

    def __str__(self):
        return self.name


class City(TimeStampedModel):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "cities"
        verbose_name_plural = "cities"

    def __str__(self):
        return self.name


class ShippingMethod(TimeStampedModel):
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estimated_days_min = models.PositiveIntegerField(default=1)
    estimated_days_max = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    is_free_above = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = "shipping_methods"

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        PROCESSING = "processing", "Processing"
        PACKAGING = "packaging", "Packaging"
        SHIPPING = "shipping", "Shipping"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    is_guest = models.BooleanField(default=False)
    guest_email = models.EmailField(blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)

    shipping_name = models.CharField(max_length=200)
    shipping_phone = models.CharField(max_length=20)
    shipping_province = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_address = models.TextField()

    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.PROTECT, null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    subtotal = models.DecimalField(max_digits=14, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2)

    coupon = models.ForeignKey("promotions.Coupon", on_delete=models.SET_NULL, null=True, blank=True)
    gift_card = models.ForeignKey("promotions.GiftCard", on_delete=models.SET_NULL, null=True, blank=True)
    wallet_amount_used = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    tracking_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    loyalty_points_earned = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        return self.order_number


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT)
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255)
    variant_sku = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=14, decimal_places=2)
    total_price = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = "order_items"


class OrderStatusHistory(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "order_status_history"
        ordering = ["-created_at"]
        verbose_name_plural = "order status histories"


class Invoice(TimeStampedModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="invoice")
    invoice_number = models.CharField(max_length=20, unique=True)
    pdf_file = models.FileField(upload_to="invoices/", blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"
