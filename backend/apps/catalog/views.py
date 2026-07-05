from django.db.models import Prefetch
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.catalog.filters import ProductFilter
from apps.catalog.models import (
    Brand,
    Category,
    Color,
    PriceAlert,
    Product,
    ProductComparison,
    ProductVariant,
    RAMOption,
    RecentlyViewed,
    StorageOption,
    Wishlist,
)
from apps.catalog.serializers import (
    BrandSerializer,
    CategorySerializer,
    ColorSerializer,
    PriceAlertSerializer,
    ProductComparisonSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ProductVariantSerializer,
    RAMOptionSerializer,
    RecentlyViewedSerializer,
    StorageOptionSerializer,
    WishlistSerializer,
)
from apps.catalog.services import CatalogService
from core.permissions.base import IsAdminUser, IsOwnerOrReadOnly
from core.utils.pagination import LargeResultsSetPagination, StandardResultsSetPagination


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ["name", "name_fa", "slug"]
    ordering_fields = ["sort_order", "name"]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"
    search_fields = ["name", "name_fa", "slug"]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "list":
            context["include_children"] = True
        return context

    def get_queryset(self):
        if self.action == "list":
            return Category.objects.filter(is_active=True, parent__isnull=True)
        return super().get_queryset()


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Color.objects.filter(is_active=True)
    serializer_class = ColorSerializer
    pagination_class = StandardResultsSetPagination


class StorageOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StorageOption.objects.filter(is_active=True)
    serializer_class = StorageOptionSerializer
    pagination_class = StandardResultsSetPagination


class RAMOptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RAMOption.objects.filter(is_active=True)
    serializer_class = RAMOptionSerializer
    pagination_class = StandardResultsSetPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True, is_deleted=False)
    pagination_class = LargeResultsSetPagination
    filterset_class = ProductFilter
    search_fields = ["name", "name_fa", "sku", "slug", "description"]
    ordering_fields = ["base_price", "created_at", "sold_count", "average_rating", "view_count"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, is_deleted=False).select_related(
            "brand", "category"
        ).prefetch_related(
            "images",
            "tags",
            Prefetch("variants", queryset=ProductVariant.objects.filter(is_active=True)),
        )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = request.META.get("REMOTE_ADDR")
        session_key = request.session.session_key or ""
        user = request.user if request.user.is_authenticated else None
        CatalogService.record_product_view(instance, user=user, session_key=session_key, ip_address=ip)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProductVariant.objects.filter(is_active=True).select_related(
        "product", "color", "storage", "ram"
    )
    serializer_class = ProductVariantSerializer
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["product"]
    search_fields = ["sku", "product__name"]


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related(
            "product", "variant", "product__brand", "product__category"
        ).prefetch_related("product__images")


class RecentlyViewedViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecentlyViewedSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return RecentlyViewed.objects.filter(user=self.request.user).select_related(
            "product", "product__brand", "product__category"
        ).prefetch_related("product__images")[:20]


class ProductComparisonViewSet(viewsets.ModelViewSet):
    serializer_class = ProductComparisonSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_queryset(self):
        return ProductComparison.objects.filter(user=self.request.user).prefetch_related(
            "products", "products__brand", "products__category"
        )

    def get_object(self):
        comparison, _ = ProductComparison.objects.get_or_create(user=self.request.user)
        return comparison

    def list(self, request, *args, **kwargs):
        comparison = self.get_object()
        serializer = self.get_serializer(comparison)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"detail": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            comparison = CatalogService.add_to_comparison(request.user, product_id)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(comparison)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def remove(self, request):
        product_id = request.data.get("product_id")
        comparison = ProductComparison.objects.filter(user=request.user).first()
        if comparison and product_id:
            comparison.products.remove(product_id)
        serializer = self.get_serializer(comparison or ProductComparison(user=request.user))
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def clear(self, request):
        comparison = ProductComparison.objects.filter(user=request.user).first()
        if comparison:
            comparison.products.clear()
        return Response({"detail": "Comparison cleared."})


class PriceAlertViewSet(viewsets.ModelViewSet):
    serializer_class = PriceAlertSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user).select_related("product", "variant")
