from django.contrib import admin

from apps.analytics.models import DailyStats, PageView


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "total_orders",
        "total_revenue",
        "total_visitors",
        "new_customers",
        "average_order_value",
    ]
    list_filter = ["date"]
    ordering = ["-date"]


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ["path", "ip_address", "session_key", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["path", "ip_address"]
