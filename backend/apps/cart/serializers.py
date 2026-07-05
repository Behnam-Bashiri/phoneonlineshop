from rest_framework import serializers

from apps.cart.models import Cart, CartItem, SavedForLater
from apps.catalog.serializers import ProductListSerializer, ProductVariantSerializer
from apps.promotions.serializers import CouponSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.IntegerField(write_only=True)
    line_total = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "variant",
            "variant_id",
            "quantity",
            "unit_price",
            "line_total",
            "created_at",
        ]
        read_only_fields = ["id", "product", "variant", "unit_price", "line_total", "created_at"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "coupon", "subtotal", "item_count", "created_at", "updated_at"]
        read_only_fields = fields


class AddToCartSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)


class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)


class SavedForLaterSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = SavedForLater
        fields = ["id", "product", "variant", "created_at"]
        read_only_fields = fields
