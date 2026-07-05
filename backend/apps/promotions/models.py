from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Coupon(TimeStampedModel):
    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed Amount"

    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    max_discount_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    usage_count = models.PositiveIntegerField(default=0)
    per_user_limit = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    applicable_categories = models.ManyToManyField("catalog.Category", blank=True)
    applicable_products = models.ManyToManyField("catalog.Product", blank=True)

    class Meta:
        db_table = "coupons"

    def __str__(self):
        return self.code


class UserCoupon(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_coupons")
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="user_assignments")
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "user_coupons"
        unique_together = ["user", "coupon"]


class GiftCard(TimeStampedModel):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    initial_balance = models.DecimalField(max_digits=14, decimal_places=2)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2)
    purchased_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="purchased_gift_cards"
    )
    recipient_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "gift_cards"


class FlashSale(TimeStampedModel):
    title = models.CharField(max_length=200)
    title_fa = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    banner_image = models.ImageField(upload_to="flash_sales/", blank=True, null=True)

    class Meta:
        db_table = "flash_sales"
        ordering = ["-starts_at"]


class FlashSaleProduct(TimeStampedModel):
    flash_sale = models.ForeignKey(FlashSale, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.CASCADE, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=14, decimal_places=2)
    stock_limit = models.PositiveIntegerField(null=True, blank=True)
    sold_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "flash_sale_products"
        unique_together = ["flash_sale", "product", "variant"]


class SpecialOffer(TimeStampedModel):
    title = models.CharField(max_length=200)
    title_fa = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="offers/")
    link_url = models.CharField(max_length=500, blank=True)
    discount_text = models.CharField(max_length=50, blank=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "special_offers"
        ordering = ["sort_order"]
