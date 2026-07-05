from rest_framework import serializers

from apps.catalog.serializers import ProductListSerializer
from apps.promotions.models import Coupon, FlashSale, FlashSaleProduct, GiftCard, SpecialOffer


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            "id",
            "code",
            "description",
            "discount_type",
            "discount_value",
            "min_order_amount",
            "max_discount_amount",
            "starts_at",
            "expires_at",
            "is_active",
        ]
        read_only_fields = fields


class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = [
            "id",
            "code",
            "initial_balance",
            "current_balance",
            "recipient_email",
            "is_active",
            "expires_at",
        ]
        read_only_fields = ["id", "code", "initial_balance", "current_balance"]


class FlashSaleProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = FlashSaleProduct
        fields = [
            "id",
            "product",
            "variant",
            "sale_price",
            "stock_limit",
            "sold_count",
        ]


class FlashSaleSerializer(serializers.ModelSerializer):
    products = FlashSaleProductSerializer(many=True, read_only=True)

    class Meta:
        model = FlashSale
        fields = [
            "id",
            "title",
            "title_fa",
            "description",
            "discount_percent",
            "starts_at",
            "ends_at",
            "is_active",
            "banner_image",
            "products",
        ]


class SpecialOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialOffer
        fields = [
            "id",
            "title",
            "title_fa",
            "description",
            "image",
            "link_url",
            "discount_text",
            "starts_at",
            "ends_at",
            "is_active",
            "sort_order",
        ]
