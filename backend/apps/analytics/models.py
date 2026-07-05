from django.db import models

from core.models import TimeStampedModel


class DailyStats(TimeStampedModel):
    date = models.DateField(unique=True, db_index=True)
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total_visitors = models.PositiveIntegerField(default=0)
    new_customers = models.PositiveIntegerField(default=0)
    products_sold = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = "daily_stats"
        ordering = ["-date"]
        verbose_name_plural = "daily stats"


class PageView(TimeStampedModel):
    path = models.CharField(max_length=500, db_index=True)
    session_key = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    referrer = models.CharField(max_length=500, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        db_table = "page_views"
        indexes = [models.Index(fields=["path", "-created_at"])]
