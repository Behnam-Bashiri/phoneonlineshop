from rest_framework import serializers

from apps.orders.models import City, Invoice, Order, OrderItem, OrderStatusHistory, Province, ShippingMethod


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "name_fa", "code", "is_active"]


class CitySerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = City
        fields = ["id", "province", "name", "name_fa", "is_active"]


class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = [
            "id",
            "name",
            "name_fa",
            "description",
            "base_cost",
            "cost_per_kg",
            "estimated_days_min",
            "estimated_days_max",
            "is_active",
            "is_free_above",
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "variant",
            "product_name",
            "variant_sku",
            "quantity",
            "unit_price",
            "total_price",
        ]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["id", "status", "note", "changed_by", "created_at"]


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "total",
            "tracking_number",
            "created_at",
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    shipping_method = ShippingMethodSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "shipping_name",
            "shipping_phone",
            "shipping_province",
            "shipping_city",
            "shipping_postal_code",
            "shipping_address",
            "shipping_method",
            "shipping_cost",
            "subtotal",
            "discount_amount",
            "tax_amount",
            "total",
            "wallet_amount_used",
            "tracking_number",
            "notes",
            "loyalty_points_earned",
            "items",
            "status_history",
            "created_at",
            "updated_at",
        ]


class CheckoutSerializer(serializers.Serializer):
    shipping_name = serializers.CharField(max_length=200)
    shipping_phone = serializers.CharField(max_length=20)
    shipping_province = serializers.CharField(max_length=100)
    shipping_city = serializers.CharField(max_length=100)
    shipping_postal_code = serializers.CharField(max_length=20)
    shipping_address = serializers.CharField()
    shipping_method_id = serializers.IntegerField(required=False, allow_null=True)
    use_wallet = serializers.BooleanField(default=False)
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["id", "invoice_number", "pdf_file", "issued_at"]
