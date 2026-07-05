from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.promotions.views import CouponViewSet, FlashSaleViewSet, SpecialOfferViewSet

router = DefaultRouter()
router.register("coupons", CouponViewSet, basename="coupon")
router.register("flash-sales", FlashSaleViewSet, basename="flash-sale")
router.register("special-offers", SpecialOfferViewSet, basename="special-offer")

urlpatterns = [
    path("", include(router.urls)),
]
