from decimal import Decimal

from django.db import transaction

from apps.cart.models import Cart, CartItem, SavedForLater
from apps.catalog.models import ProductVariant
from apps.promotions.services import CouponService


class CartService:
    @staticmethod
    def get_or_create_cart(user=None, session_key=""):
        if user and user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
            return cart
        if session_key:
            cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
            return cart
        raise ValueError("User or session_key required.")

    @staticmethod
    @transaction.atomic
    def add_item(cart, variant_id, quantity=1):
        variant = ProductVariant.objects.select_related("product").get(
            pk=variant_id, is_active=True, product__is_active=True
        )
        if variant.available_stock < quantity:
            raise ValueError("Insufficient stock.")

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            variant=variant,
            defaults={
                "product": variant.product,
                "quantity": quantity,
                "unit_price": variant.price,
            },
        )
        if not created:
            new_qty = item.quantity + quantity
            if variant.available_stock < new_qty:
                raise ValueError("Insufficient stock.")
            item.quantity = new_qty
            item.unit_price = variant.price
            item.save()
        return item

    @staticmethod
    def update_item_quantity(cart, item_id, quantity):
        item = CartItem.objects.select_related("variant").get(pk=item_id, cart=cart)
        if quantity <= 0:
            item.delete()
            return None
        if item.variant.available_stock < quantity:
            raise ValueError("Insufficient stock.")
        item.quantity = quantity
        item.save()
        return item

    @staticmethod
    def remove_item(cart, item_id):
        CartItem.objects.filter(pk=item_id, cart=cart).delete()

    @staticmethod
    def clear_cart(cart):
        cart.items.all().delete()

    @staticmethod
    def apply_coupon(cart, coupon_code):
        coupon = CouponService.validate_coupon(coupon_code, cart.user, cart.subtotal)
        cart.coupon = coupon
        cart.save(update_fields=["coupon", "updated_at"])
        return coupon

    @staticmethod
    def remove_coupon(cart):
        cart.coupon = None
        cart.save(update_fields=["coupon", "updated_at"])

    @staticmethod
    def get_cart_totals(cart):
        subtotal = cart.subtotal
        discount = Decimal("0")
        if cart.coupon:
            discount = CouponService.calculate_discount(cart.coupon, subtotal, cart.user)
        return {
            "subtotal": subtotal,
            "discount": discount,
            "total": max(Decimal("0"), subtotal - discount),
            "item_count": cart.item_count,
        }

    @staticmethod
    @transaction.atomic
    def save_for_later(user, item_id):
        item = CartItem.objects.select_related("variant", "product", "cart").get(pk=item_id)
        if item.cart.user != user:
            raise ValueError("Item does not belong to user cart.")
        SavedForLater.objects.get_or_create(
            user=user,
            product=item.product,
            variant=item.variant,
        )
        item.delete()

    @staticmethod
    @transaction.atomic
    def move_to_cart(user, saved_id):
        saved = SavedForLater.objects.select_related("variant", "product").get(pk=saved_id, user=user)
        cart = CartService.get_or_create_cart(user=user)
        CartService.add_item(cart, saved.variant_id, quantity=1)
        saved.delete()
