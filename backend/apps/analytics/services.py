from datetime import timedelta
from decimal import Decimal

from django.db.models import Count, Sum
from django.utils import timezone

from apps.accounts.models import User
from apps.analytics.models import DailyStats, PageView
from apps.orders.models import Order


class AnalyticsService:
    @staticmethod
    def get_dashboard_stats(days=30):
        since = timezone.now() - timedelta(days=days)
        today = timezone.now().date()

        orders = Order.objects.filter(created_at__gte=since)
        order_stats = orders.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("total"),
        )

        today_orders = Order.objects.filter(created_at__date=today)
        today_stats = today_orders.aggregate(
            orders=Count("id"),
            revenue=Sum("total"),
        )

        new_customers = User.objects.filter(date_joined__gte=since).count()
        page_views = PageView.objects.filter(created_at__gte=since).count()

        daily_stats = DailyStats.objects.order_by("-date")[:days]

        return {
            "period_days": days,
            "total_orders": order_stats["total_orders"] or 0,
            "total_revenue": str(order_stats["total_revenue"] or Decimal("0")),
            "today_orders": today_stats["orders"] or 0,
            "today_revenue": str(today_stats["revenue"] or Decimal("0")),
            "new_customers": new_customers,
            "page_views": page_views,
            "daily_stats": [
                {
                    "date": stat.date.isoformat(),
                    "total_orders": stat.total_orders,
                    "total_revenue": str(stat.total_revenue),
                    "total_visitors": stat.total_visitors,
                    "new_customers": stat.new_customers,
                    "products_sold": stat.products_sold,
                    "average_order_value": str(stat.average_order_value),
                }
                for stat in daily_stats
            ],
        }

    @staticmethod
    def record_page_view(path, session_key="", ip_address=None, referrer="", user_agent=""):
        return PageView.objects.create(
            path=path,
            session_key=session_key,
            ip_address=ip_address,
            referrer=referrer,
            user_agent=user_agent,
        )
