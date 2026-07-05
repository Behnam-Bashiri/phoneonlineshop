import uuid
from django.utils import timezone

from django.db import transaction

from apps.orders.models import Order
from apps.payments.models import Payment, PaymentLog


class PaymentService:
    @staticmethod
    @transaction.atomic
    def initiate_payment(order, user, method=Payment.Method.ONLINE):
        existing = Payment.objects.filter(
            order=order,
            status__in=[Payment.Status.PENDING, Payment.Status.PROCESSING],
        ).first()
        if existing:
            return existing

        payment = Payment.objects.create(
            order=order,
            user=user,
            amount=order.total,
            method=method,
            status=Payment.Status.PENDING,
            gateway="mock",
        )
        PaymentLog.objects.create(
            payment=payment,
            event="initiated",
            data={"order_number": order.order_number, "amount": str(order.total)},
        )
        return payment

    @staticmethod
    @transaction.atomic
    def process_mock_payment(payment_id, success=True, ip_address=None):
        payment = Payment.objects.select_for_update().select_related("order").get(pk=payment_id)

        if payment.status not in [Payment.Status.PENDING, Payment.Status.PROCESSING]:
            raise ValueError("Payment is not in a processable state.")

        payment.status = Payment.Status.PROCESSING
        payment.save(update_fields=["status", "updated_at"])

        PaymentLog.objects.create(
            payment=payment,
            event="processing",
            data={"gateway": "mock"},
            ip_address=ip_address,
        )

        if success:
            payment.status = Payment.Status.COMPLETED
            payment.transaction_id = f"MOCK-{uuid.uuid4().hex[:12].upper()}"
            payment.paid_at = timezone.now()
            payment.gateway_response = {"status": "success", "gateway": "mock"}
            payment.save()

            order = payment.order
            order.status = Order.Status.PAID
            order.save(update_fields=["status", "updated_at"])

            from apps.orders.models import OrderStatusHistory

            OrderStatusHistory.objects.create(
                order=order,
                status=Order.Status.PAID,
                note="Payment completed via mock gateway",
            )

            PaymentLog.objects.create(
                payment=payment,
                event="completed",
                data={"transaction_id": payment.transaction_id},
                ip_address=ip_address,
            )
        else:
            payment.status = Payment.Status.FAILED
            payment.gateway_response = {"status": "failed", "gateway": "mock"}
            payment.save()
            PaymentLog.objects.create(
                payment=payment,
                event="failed",
                data={"reason": "mock_failure"},
                ip_address=ip_address,
            )

        return payment

    @staticmethod
    def get_payment_status(payment_id):
        payment = Payment.objects.select_related("order").get(pk=payment_id)
        return {
            "id": str(payment.id),
            "status": payment.status,
            "amount": payment.amount,
            "method": payment.method,
            "transaction_id": payment.transaction_id,
            "paid_at": payment.paid_at,
            "order_number": payment.order.order_number,
        }
