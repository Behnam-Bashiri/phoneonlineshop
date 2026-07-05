from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.inventory.views import (
    InventoryItemViewSet,
    StockMovementViewSet,
    SupplierViewSet,
    WarehouseViewSet,
)

router = DefaultRouter()
router.register("warehouses", WarehouseViewSet, basename="warehouse")
router.register("suppliers", SupplierViewSet, basename="supplier")
router.register("items", InventoryItemViewSet, basename="inventory-item")
router.register("movements", StockMovementViewSet, basename="stock-movement")

urlpatterns = [
    path("", include(router.urls)),
]
