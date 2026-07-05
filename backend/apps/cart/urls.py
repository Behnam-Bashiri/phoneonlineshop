from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.cart.views import (
    ApplyCouponView,
    CartItemView,
    CartView,
    MoveToCartView,
    SaveForLaterView,
    SavedForLaterViewSet,
)

router = DefaultRouter()
router.register("saved", SavedForLaterViewSet, basename="saved-for-later")

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("items/<int:item_id>/", CartItemView.as_view(), name="cart-item"),
    path("coupon/", ApplyCouponView.as_view(), name="cart-coupon"),
    path("items/<int:item_id>/save/", SaveForLaterView.as_view(), name="save-for-later"),
    path("saved/<int:saved_id>/move/", MoveToCartView.as_view(), name="move-to-cart"),
] + router.urls
