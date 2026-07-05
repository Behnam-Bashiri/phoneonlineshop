import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from core.models import SoftDeleteModel, TimeStampedModel


class Brand(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    name_fa = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, max_length=120)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        db_table = "brands"
        ordering = ["sort_order", "name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(MPTTModel, TimeStampedModel):
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, max_length=120)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    class MPTTMeta:
        order_insertion_by = ["sort_order", "name"]

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Color(TimeStampedModel):
    name = models.CharField(max_length=50)
    name_fa = models.CharField(max_length=50, blank=True)
    hex_code = models.CharField(max_length=7)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "colors"

    def __str__(self):
        return self.name


class StorageOption(TimeStampedModel):
    capacity = models.CharField(max_length=20)
    capacity_gb = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "storage_options"
        ordering = ["capacity_gb"]

    def __str__(self):
        return self.capacity


class RAMOption(TimeStampedModel):
    capacity = models.CharField(max_length=20)
    capacity_gb = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "ram_options"
        ordering = ["capacity_gb"]

    def __str__(self):
        return self.capacity


class Product(SoftDeleteModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    name_fa = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=280)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    barcode = models.CharField(max_length=50, blank=True, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True)
    description_fa = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)
    base_price = models.DecimalField(max_digits=14, decimal_places=2)
    compare_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    has_360_view = models.BooleanField(default=False)
    warranty_months = models.PositiveIntegerField(default=12)
    weight_grams = models.PositiveIntegerField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="products/og/", blank=True, null=True)
    tags = TaggableManager(blank=True)
    advantages = models.JSONField(default=list, blank=True)
    disadvantages = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["-view_count"]),
            models.Index(fields=["-sold_count"]),
            models.Index(fields=["-average_rating"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    color = models.ForeignKey(Color, on_delete=models.PROTECT, null=True, blank=True)
    storage = models.ForeignKey(StorageOption, on_delete=models.PROTECT, null=True, blank=True)
    ram = models.ForeignKey(RAMOption, on_delete=models.PROTECT, null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    compare_price = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    image = models.ImageField(upload_to="variants/", blank=True, null=True)

    class Meta:
        db_table = "product_variants"
        unique_together = [["product", "color", "storage", "ram"]]

    @property
    def available_stock(self):
        return max(0, self.stock_quantity - self.reserved_quantity)

    def __str__(self):
        return f"{self.product.name} - {self.sku}"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "product_images"
        ordering = ["sort_order"]


class ProductVideo(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="videos")
    title = models.CharField(max_length=200, blank=True)
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to="products/videos/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="products/video_thumbs/", blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "product_videos"
        ordering = ["sort_order"]


class ProductSpecification(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    group_name = models.CharField(max_length=100)
    group_name_fa = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    value = models.CharField(max_length=500)
    value_fa = models.CharField(max_length=500, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "product_specifications"
        ordering = ["group_name", "sort_order"]


class ProductView(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "product_views"


class PriceHistory(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_history")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "price_history"
        ordering = ["-recorded_at"]


class PriceAlert(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="price_alerts")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_alerts")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    target_price = models.DecimalField(max_digits=14, decimal_places=2)
    is_active = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)

    class Meta:
        db_table = "price_alerts"
        unique_together = ["user", "product", "variant"]


class Wishlist(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = "wishlist"
        unique_together = ["user", "product", "variant"]


class RecentlyViewed(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recently_viewed")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "recently_viewed"
        ordering = ["-viewed_at"]
        unique_together = ["user", "product"]


class ProductComparison(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comparisons")
    products = models.ManyToManyField(Product, related_name="comparisons")
    session_key = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "product_comparisons"


class Accessory(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="accessories")
    accessory_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="accessory_for")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "accessories"
        unique_together = ["product", "accessory_product"]
