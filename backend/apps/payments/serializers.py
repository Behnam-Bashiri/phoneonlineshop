from rest_framework import serializers

from apps.payments.models import Payment, PaymentLog


class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source="order.order_number", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "order_number",
            "amount",
            "method",
            "status",
            "gateway",
            "transaction_id",
            "paid_at",
            "created_at",
        ]
        read_only_fields = fields


class PaymentLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentLog
        fields = ["id", "event", "data", "ip_address", "created_at"]
        read_only_fields = fields


class InitiatePaymentSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    method = serializers.ChoiceField(choices=Payment.Method.choices, default=Payment.Method.ONLINE)


class MockPaymentSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
