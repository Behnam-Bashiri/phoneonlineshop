from rest_framework import serializers

from apps.analytics.models import DailyStats, PageView


class DailyStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStats
        fields = [
            "date",
            "total_orders",
            "total_revenue",
            "total_visitors",
            "new_customers",
            "products_sold",
            "average_order_value",
        ]


class DashboardStatsSerializer(serializers.Serializer):
    period_days = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    total_revenue = serializers.CharField()
    today_orders = serializers.IntegerField()
    today_revenue = serializers.CharField()
    new_customers = serializers.IntegerField()
    page_views = serializers.IntegerField()
    daily_stats = DailyStatsSerializer(many=True)
