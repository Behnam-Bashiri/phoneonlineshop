from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Cart(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="cart"
    )
    session_key = models.CharField(max_length=255, blank=True, db_index=True)
    coupon = models.ForeignKey("promotions.Coupon", on_delete=models.SET_NULL, null=True, blank=True)
    gift_card = models.ForeignKey("promotions.GiftCard", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "carts"

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.all())

    @property
    def item_count(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        db_table = "cart_items"
        unique_together = ["cart", "variant"]

    @property
    def line_total(self):
        return self.unit_price * self.quantity


class SavedForLater(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.CASCADE)

    class Meta:
        db_table = "saved_for_later"
        unique_together = ["user", "variant"]
