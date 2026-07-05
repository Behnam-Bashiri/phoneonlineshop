from django.contrib import admin

from apps.cart.models import Cart, CartItem, SavedForLater


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "session_key", "coupon", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__email", "session_key"]
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "variant", "quantity", "unit_price"]
    search_fields = ["product__name", "variant__sku"]


@admin.register(SavedForLater)
class SavedForLaterAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "variant", "created_at"]
    search_fields = ["user__email", "product__name"]
