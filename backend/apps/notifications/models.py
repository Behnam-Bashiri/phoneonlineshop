from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Notification(TimeStampedModel):
    class NotificationType(models.TextChoices):
        ORDER = "order", "Order"
        PAYMENT = "payment", "Payment"
        PROMOTION = "promotion", "Promotion"
        SYSTEM = "system", "System"
        SUPPORT = "support", "Support"
        WALLET = "wallet", "Wallet"
        CLUB = "club", "Customer Club"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    title_fa = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    message_fa = models.TextField(blank=True)
    link = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]


class NotificationTemplate(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    notification_type = models.CharField(max_length=20, choices=Notification.NotificationType.choices)
    title_template = models.CharField(max_length=255)
    message_template = models.TextField()
    email_template = models.TextField(blank=True)
    sms_template = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "notification_templates"
