from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order
from apps.support.models import SupportTicket, TicketDepartment
from apps.support.serializers import (
    CreateTicketSerializer,
    SupportTicketDetailSerializer,
    SupportTicketListSerializer,
    TicketDepartmentSerializer,
    TicketReplyCreateSerializer,
    TicketReplySerializer,
)
from apps.support.services import SupportService
from core.permissions.base import IsAdminUser, IsOwnerOrReadOnly
from core.utils.pagination import StandardResultsSetPagination


class TicketDepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketDepartment.objects.filter(is_active=True)
    serializer_class = TicketDepartmentSerializer
    pagination_class = StandardResultsSetPagination


class SupportTicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    lookup_field = "ticket_number"
    http_method_names = ["get", "post", "head", "options"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SupportTicketDetailSerializer
        return SupportTicketListSerializer

    def get_queryset(self):
        queryset = SupportTicket.objects.select_related("department", "order")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = CreateTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        department = TicketDepartment.objects.filter(pk=data["department_id"], is_active=True).first()
        if not department:
            return Response({"detail": "Invalid department."}, status=status.HTTP_400_BAD_REQUEST)

        order = None
        if data.get("order_id"):
            order = Order.objects.filter(pk=data["order_id"], user=request.user).first()

        ticket = SupportService.create_ticket(
            user=request.user,
            department=department,
            subject=data["subject"],
            message=data["message"],
            priority=data.get("priority"),
            order=order,
        )
        return Response(
            SupportTicketDetailSerializer(ticket, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def reply(self, request, ticket_number=None):
        ticket = self.get_object()
        serializer = TicketReplyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reply = SupportService.add_reply(ticket, request.user, serializer.validated_data["message"])
        return Response(
            TicketReplySerializer(reply, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )
