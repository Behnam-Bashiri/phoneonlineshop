from django.contrib import admin

from apps.promotions.models import Coupon, FlashSale, FlashSaleProduct, GiftCard, SpecialOffer, UserCoupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["code", "discount_type", "discount_value", "usage_count", "is_active", "expires_at"]
    list_filter = ["discount_type", "is_active"]
    search_fields = ["code", "description"]
    filter_horizontal = ["applicable_categories", "applicable_products"]


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ["user", "coupon", "is_used", "used_at"]
    list_filter = ["is_used"]
    search_fields = ["user__email", "coupon__code"]


@admin.register(GiftCard)
class GiftCardAdmin(admin.ModelAdmin):
    list_display = ["code", "current_balance", "purchased_by", "is_active", "expires_at"]
    list_filter = ["is_active"]
    search_fields = ["code", "recipient_email"]


class FlashSaleProductInline(admin.TabularInline):
    model = FlashSaleProduct
    extra = 1


@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ["title", "discount_percent", "starts_at", "ends_at", "is_active"]
    list_filter = ["is_active"]
    inlines = [FlashSaleProductInline]


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ["title", "discount_text", "is_active", "sort_order"]
    list_filter = ["is_active"]
    search_fields = ["title", "title_fa"]
