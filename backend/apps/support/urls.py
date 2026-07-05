from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.support.views import SupportTicketViewSet, TicketDepartmentViewSet

router = DefaultRouter()
router.register("departments", TicketDepartmentViewSet, basename="ticket-department")
router.register("tickets", SupportTicketViewSet, basename="support-ticket")

urlpatterns = [
    path("", include(router.urls)),
]
