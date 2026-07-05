from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.serializers import InitiatePaymentSerializer, MockPaymentSerializer, PaymentSerializer
from apps.payments.services import PaymentService
from core.permissions.base import IsOwnerOrReadOnly
from core.utils.pagination import StandardResultsSetPagination


class PaymentViewSet(ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related("order")


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            order = Order.objects.get(
                pk=serializer.validated_data["order_id"],
                user=request.user,
            )
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status != Order.Status.PENDING:
            return Response({"detail": "Order is not payable."}, status=status.HTTP_400_BAD_REQUEST)

        payment = PaymentService.initiate_payment(
            order,
            request.user,
            method=serializer.validated_data.get("method", Payment.Method.ONLINE),
        )
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)


class MockPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, payment_id):
        serializer = MockPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            payment = Payment.objects.get(pk=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

        ip = request.META.get("REMOTE_ADDR")
        try:
            payment = PaymentService.process_mock_payment(
                payment.id,
                success=serializer.validated_data.get("success", True),
                ip_address=ip,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PaymentSerializer(payment).data)


class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(pk=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(PaymentService.get_payment_status(payment.id))
