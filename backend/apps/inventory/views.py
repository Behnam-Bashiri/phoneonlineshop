from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.inventory.models import InventoryItem, StockMovement, Supplier, Warehouse
from apps.inventory.serializers import (
    InventoryItemSerializer,
    StockMovementSerializer,
    SupplierSerializer,
    WarehouseSerializer,
)
from core.permissions.base import IsAdminUser
from core.utils.pagination import StandardResultsSetPagination


class WarehouseViewSet(ReadOnlyModelViewSet):
    queryset = Warehouse.objects.filter(is_active=True)
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination


class SupplierViewSet(ReadOnlyModelViewSet):
    queryset = Supplier.objects.filter(is_active=True)
    serializer_class = SupplierSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination


class InventoryItemViewSet(ReadOnlyModelViewSet):
    queryset = InventoryItem.objects.select_related("variant", "warehouse", "supplier")
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["warehouse", "variant"]


class StockMovementViewSet(ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related("variant", "warehouse", "performed_by")
    serializer_class = StockMovementSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["movement_type", "warehouse"]
