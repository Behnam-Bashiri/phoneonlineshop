from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.catalog.views import (
    BrandViewSet,
    CategoryViewSet,
    ColorViewSet,
    PriceAlertViewSet,
    ProductComparisonViewSet,
    ProductVariantViewSet,
    ProductViewSet,
    RAMOptionViewSet,
    RecentlyViewedViewSet,
    StorageOptionViewSet,
    WishlistViewSet,
)

router = DefaultRouter()
router.register("brands", BrandViewSet, basename="brand")
router.register("categories", CategoryViewSet, basename="category")
router.register("colors", ColorViewSet, basename="color")
router.register("storage-options", StorageOptionViewSet, basename="storage-option")
router.register("ram-options", RAMOptionViewSet, basename="ram-option")
router.register("products", ProductViewSet, basename="product")
router.register("variants", ProductVariantViewSet, basename="variant")
router.register("wishlist", WishlistViewSet, basename="wishlist")
router.register("recently-viewed", RecentlyViewedViewSet, basename="recently-viewed")
router.register("compare", ProductComparisonViewSet, basename="compare")
router.register("price-alerts", PriceAlertViewSet, basename="price-alert")

urlpatterns = [
    path("", include(router.urls)),
]
