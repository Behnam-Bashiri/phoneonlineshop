from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.filters import OrderFilter
from apps.orders.models import City, Order, Province, ShippingMethod
from apps.orders.serializers import (
    CheckoutSerializer,
    CitySerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    ProvinceSerializer,
    ShippingMethodSerializer,
)
from apps.orders.services import OrderService
from core.permissions.base import IsAdminUser, IsOwnerOrReadOnly
from core.utils.pagination import StandardResultsSetPagination


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.filter(is_active=True)
    serializer_class = ProvinceSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ["name", "name_fa", "code"]


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.filter(is_active=True).select_related("province")
    serializer_class = CitySerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["province"]
    search_fields = ["name", "name_fa"]


class ShippingMethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShippingMethod.objects.filter(is_active=True)
    serializer_class = ShippingMethodSerializer
    pagination_class = StandardResultsSetPagination


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_class = OrderFilter
    search_fields = ["order_number", "tracking_number"]
    ordering_fields = ["created_at", "total", "status"]
    lookup_field = "order_number"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderListSerializer

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items", "status_history")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    @action(detail=True, methods=["get"])
    def tracking(self, request, order_number=None):
        order = self.get_object()
        history = order.status_history.all()
        from apps.orders.serializers import OrderStatusHistorySerializer

        return Response({
            "order_number": order.order_number,
            "status": order.status,
            "tracking_number": order.tracking_number,
            "history": OrderStatusHistorySerializer(history, many=True).data,
        })


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = OrderService.checkout(
                user=request.user,
                shipping_data=serializer.validated_data,
                shipping_method_id=serializer.validated_data.get("shipping_method_id"),
                use_wallet=serializer.validated_data.get("use_wallet", False),
                notes=serializer.validated_data.get("notes", ""),
            )
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        from apps.notifications.tasks import send_order_confirmation_email

        send_order_confirmation_email.delay(str(request.user.id), order.order_number, str(order.total))
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)
