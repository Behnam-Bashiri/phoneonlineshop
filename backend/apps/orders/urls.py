from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.orders.views import CheckoutView, CityViewSet, OrderViewSet, ProvinceViewSet, ShippingMethodViewSet

router = DefaultRouter()
router.register("provinces", ProvinceViewSet, basename="province")
router.register("cities", CityViewSet, basename="city")
router.register("shipping-methods", ShippingMethodViewSet, basename="shipping-method")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", include(router.urls)),
]
