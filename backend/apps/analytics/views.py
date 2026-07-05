from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.analytics.models import DailyStats
from apps.analytics.serializers import DailyStatsSerializer, DashboardStatsSerializer
from apps.analytics.services import AnalyticsService
from core.utils.pagination import StandardResultsSetPagination


class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        stats = AnalyticsService.get_dashboard_stats(days=days)
        return Response(stats)


class DailyStatsViewSet(ReadOnlyModelViewSet):
    queryset = DailyStats.objects.all()
    serializer_class = DailyStatsSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
