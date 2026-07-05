import random
import string
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.accounts.services import WalletService
from apps.cart.services import CartService
from apps.cms.models import SiteSettings
from apps.orders.models import Invoice, Order, OrderItem, OrderStatusHistory
from apps.promotions.services import CouponService


class OrderService:
    @staticmethod
    def generate_order_number():
        prefix = timezone.now().strftime("%y%m%d")
        suffix = "".join(random.choices(string.digits, k=6))
        return f"PS{prefix}{suffix}"

    @staticmethod
    def generate_invoice_number():
        return f"INV{timezone.now().strftime('%y%m%d')}{''.join(random.choices(string.digits, k=6))}"

    @staticmethod
    def calculate_shipping_cost(shipping_method, subtotal, weight_kg=0):
        if not shipping_method:
            return Decimal("0")
        if shipping_method.is_free_above and subtotal >= shipping_method.is_free_above:
            return Decimal("0")
        return shipping_method.base_cost + (shipping_method.cost_per_kg * Decimal(str(weight_kg)))

    @staticmethod
    def get_tax_rate():
        settings = SiteSettings.objects.first()
        if settings:
            return settings.tax_rate / Decimal("100")
        return Decimal("0.09")

    @classmethod
    @transaction.atomic
    def checkout(cls, user, shipping_data, shipping_method_id=None, use_wallet=False, notes=""):
        cart = CartService.get_or_create_cart(user=user)
        if not cart.items.exists():
            raise ValueError("Cart is empty.")

        totals = CartService.get_cart_totals(cart)
        subtotal = totals["subtotal"]
        discount = totals["discount"]

        from apps.orders.models import ShippingMethod

        shipping_method = None
        if shipping_method_id:
            shipping_method = ShippingMethod.objects.filter(pk=shipping_method_id, is_active=True).first()
            if not shipping_method:
                raise ValueError("Invalid shipping method.")

        shipping_cost = cls.calculate_shipping_cost(shipping_method, subtotal)
        taxable = subtotal - discount
        tax_amount = (taxable * cls.get_tax_rate()).quantize(Decimal("0.01"))
        total = taxable + tax_amount + shipping_cost

        wallet_amount = Decimal("0")
        if use_wallet and hasattr(user, "wallet"):
            wallet = WalletService.get_or_create_wallet(user)
            wallet_amount = min(wallet.balance, total)
            total -= wallet_amount

        order = Order.objects.create(
            order_number=cls.generate_order_number(),
            user=user,
            status=Order.Status.PENDING,
            shipping_name=shipping_data["shipping_name"],
            shipping_phone=shipping_data["shipping_phone"],
            shipping_province=shipping_data["shipping_province"],
            shipping_city=shipping_data["shipping_city"],
            shipping_postal_code=shipping_data["shipping_postal_code"],
            shipping_address=shipping_data["shipping_address"],
            shipping_method=shipping_method,
            shipping_cost=shipping_cost,
            subtotal=subtotal,
            discount_amount=discount,
            tax_amount=tax_amount,
            total=total,
            coupon=cart.coupon,
            wallet_amount_used=wallet_amount,
            notes=notes,
        )

        for item in cart.items.select_related("product", "variant"):
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                product_name=item.product.name,
                variant_sku=item.variant.sku,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.line_total,
            )
            item.variant.reserved_quantity += item.quantity
            item.variant.save(update_fields=["reserved_quantity"])

        OrderStatusHistory.objects.create(order=order, status=Order.Status.PENDING, note="Order created")

        if cart.coupon:
            CouponService.apply_coupon_usage(cart.coupon, user)

        if wallet_amount > 0:
            WalletService.withdraw(
                WalletService.get_or_create_wallet(user),
                wallet_amount,
                description=f"Order {order.order_number}",
                reference_id=order.order_number,
                order=order,
            )

        CartService.clear_cart(cart)
        cart.coupon = None
        cart.save(update_fields=["coupon"])

        Invoice.objects.create(order=order, invoice_number=cls.generate_invoice_number())
        return order

    @staticmethod
    def update_order_status(order, new_status, changed_by=None, note=""):
        order.status = new_status
        order.save(update_fields=["status", "updated_at"])
        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            note=note,
            changed_by=changed_by,
        )
        return order
