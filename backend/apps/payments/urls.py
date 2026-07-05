from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payments.views import InitiatePaymentView, MockPaymentView, PaymentStatusView, PaymentViewSet

router = DefaultRouter()
router.register("", PaymentViewSet, basename="payment")

urlpatterns = [
    path("initiate/", InitiatePaymentView.as_view(), name="payment-initiate"),
    path("<uuid:payment_id>/mock/", MockPaymentView.as_view(), name="payment-mock"),
    path("<uuid:payment_id>/status/", PaymentStatusView.as_view(), name="payment-status"),
    path("", include(router.urls)),
]
