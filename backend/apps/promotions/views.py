from django.utils import timezone
from rest_framework import viewsets

from apps.promotions.models import Coupon, FlashSale, SpecialOffer
from apps.promotions.serializers import CouponSerializer, FlashSaleSerializer, SpecialOfferSerializer
from core.permissions.base import IsAdminUser
from core.utils.pagination import StandardResultsSetPagination


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "code"
    search_fields = ["code", "description"]

    def get_queryset(self):
        now = timezone.now()
        return Coupon.objects.filter(
            is_active=True,
        ).exclude(
            expires_at__lt=now,
        )


class FlashSaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlashSale.objects.filter(is_active=True).prefetch_related("products__product")
    serializer_class = FlashSaleSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        now = timezone.now()
        return FlashSale.objects.filter(
            is_active=True,
            starts_at__lte=now,
            ends_at__gte=now,
        ).prefetch_related("products__product", "products__variant")


class SpecialOfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SpecialOffer.objects.filter(is_active=True)
    serializer_class = SpecialOfferSerializer
    pagination_class = StandardResultsSetPagination
    ordering_fields = ["sort_order"]
