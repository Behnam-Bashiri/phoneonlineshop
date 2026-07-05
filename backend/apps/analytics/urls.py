from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.analytics.views import DailyStatsViewSet, DashboardStatsView

router = DefaultRouter()
router.register("daily", DailyStatsViewSet, basename="daily-stats")

urlpatterns = [
    path("dashboard/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("", include(router.urls)),
]
