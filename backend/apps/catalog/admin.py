from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from apps.catalog.models import (
    Accessory,
    Brand,
    Category,
    Color,
    PriceAlert,
    PriceHistory,
    Product,
    ProductComparison,
    ProductImage,
    ProductSpecification,
    ProductVariant,
    ProductVideo,
    ProductView,
    RAMOption,
    RecentlyViewed,
    StorageOption,
    Wishlist,
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "name_fa", "slug", "is_active", "sort_order"]
    list_filter = ["is_active"]
    search_fields = ["name", "name_fa", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ["name", "name_fa", "slug", "is_active", "sort_order"]
    list_filter = ["is_active"]
    search_fields = ["name", "name_fa", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    mptt_level_indent = 20


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name", "hex_code", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "name_fa"]


@admin.register(StorageOption)
class StorageOptionAdmin(admin.ModelAdmin):
    list_display = ["capacity", "capacity_gb", "is_active"]
    list_filter = ["is_active"]


@admin.register(RAMOption)
class RAMOptionAdmin(admin.ModelAdmin):
    list_display = ["capacity", "capacity_gb", "is_active"]
    list_filter = ["is_active"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sku",
        "brand",
        "category",
        "base_price",
        "is_active",
        "is_featured",
        "sold_count",
    ]
    list_filter = ["is_active", "is_featured", "is_new_arrival", "is_best_seller", "brand", "category"]
    search_fields = ["name", "name_fa", "sku", "slug", "barcode"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline, ProductImageInline]
    readonly_fields = ["view_count", "sold_count", "average_rating", "review_count"]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ["product", "sku", "price", "stock_quantity", "is_active", "is_default"]
    list_filter = ["is_active", "color", "storage", "ram"]
    search_fields = ["sku", "product__name"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "variant", "sort_order", "is_primary"]
    list_filter = ["is_primary"]


@admin.register(ProductVideo)
class ProductVideoAdmin(admin.ModelAdmin):
    list_display = ["product", "title", "sort_order"]


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ["product", "group_name", "name", "value", "sort_order"]
    search_fields = ["product__name", "name", "value"]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "variant", "created_at"]
    search_fields = ["user__email", "product__name"]


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "viewed_at"]
    search_fields = ["user__email", "product__name"]


@admin.register(PriceAlert)
class PriceAlertAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "target_price", "is_active", "notified"]
    list_filter = ["is_active", "notified"]
    search_fields = ["user__email", "product__name"]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ["product", "variant", "price", "recorded_at"]
    list_filter = ["recorded_at"]


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "ip_address", "created_at"]
    list_filter = ["created_at"]


@admin.register(ProductComparison)
class ProductComparisonAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    filter_horizontal = ["products"]


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ["product", "accessory_product", "sort_order"]
