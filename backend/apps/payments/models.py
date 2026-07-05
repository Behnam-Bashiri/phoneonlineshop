import uuid

from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Payment(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"
        CANCELLED = "cancelled", "Cancelled"

    class Method(models.TextChoices):
        ONLINE = "online", "Online Gateway"
        WALLET = "wallet", "Wallet"
        COD = "cod", "Cash on Delivery"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="payments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    method = models.CharField(max_length=20, choices=Method.choices, default=Method.ONLINE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    gateway = models.CharField(max_length=50, default="mock")
    transaction_id = models.CharField(max_length=100, blank=True, db_index=True)
    gateway_response = models.JSONField(default=dict, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "payments"
        ordering = ["-created_at"]


class PaymentLog(TimeStampedModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="logs")
    event = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "payment_logs"
        ordering = ["-created_at"]
