from decimal import Decimal

from django.utils import timezone

from apps.promotions.models import Coupon, UserCoupon


class CouponService:
    @staticmethod
    def validate_coupon(code, user, order_amount):
        coupon = Coupon.objects.filter(code__iexact=code, is_active=True).first()
        if not coupon:
            raise ValueError("Invalid coupon code.")

        now = timezone.now()
        if coupon.starts_at and now < coupon.starts_at:
            raise ValueError("Coupon is not yet active.")
        if coupon.expires_at and now > coupon.expires_at:
            raise ValueError("Coupon has expired.")
        if coupon.usage_limit and coupon.usage_count >= coupon.usage_limit:
            raise ValueError("Coupon usage limit reached.")
        if order_amount < coupon.min_order_amount:
            raise ValueError(f"Minimum order amount is {coupon.min_order_amount}.")

        if user and user.is_authenticated:
            user_usage = UserCoupon.objects.filter(user=user, coupon=coupon, is_used=True).count()
            if user_usage >= coupon.per_user_limit:
                raise ValueError("You have already used this coupon.")

        return coupon

    @staticmethod
    def calculate_discount(coupon, subtotal, user=None):
        if coupon.discount_type == Coupon.DiscountType.PERCENTAGE:
            discount = subtotal * (coupon.discount_value / Decimal("100"))
            if coupon.max_discount_amount:
                discount = min(discount, coupon.max_discount_amount)
        else:
            discount = coupon.discount_value
        return min(discount, subtotal)

    @staticmethod
    def apply_coupon_usage(coupon, user):
        coupon.usage_count += 1
        coupon.save(update_fields=["usage_count"])
        if user and user.is_authenticated:
            user_coupon, _ = UserCoupon.objects.get_or_create(user=user, coupon=coupon)
            user_coupon.is_used = True
            user_coupon.used_at = timezone.now()
            user_coupon.save()
