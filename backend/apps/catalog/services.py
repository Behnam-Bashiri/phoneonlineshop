from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from apps.catalog.models import PriceAlert, Product, ProductView, RecentlyViewed, Wishlist
from apps.catalog.models import ProductComparison


class CatalogService:
    @staticmethod
    def record_product_view(product, user=None, session_key="", ip_address=None):
        ProductView.objects.create(
            product=product,
            user=user,
            session_key=session_key,
            ip_address=ip_address,
        )
        product.view_count += 1
        product.save(update_fields=["view_count"])

        if user and user.is_authenticated:
            RecentlyViewed.objects.update_or_create(
                user=user,
                product=product,
                defaults={"viewed_at": timezone.now()},
            )

    @staticmethod
    def toggle_wishlist(user, product, variant=None):
        existing = Wishlist.objects.filter(user=user, product=product, variant=variant).first()
        if existing:
            existing.delete()
            return False
        Wishlist.objects.create(user=user, product=product, variant=variant)
        return True

    @staticmethod
    def get_or_create_comparison(user, session_key=""):
        comparison, _ = ProductComparison.objects.get_or_create(
            user=user,
            defaults={"session_key": session_key},
        )
        return comparison

    @staticmethod
    def add_to_comparison(user, product_id, max_products=4):
        comparison = ProductComparison.objects.filter(user=user).first()
        if not comparison:
            comparison = ProductComparison.objects.create(user=user)
        if comparison.products.count() >= max_products:
            raise ValueError(f"Maximum {max_products} products allowed in comparison.")
        product = Product.objects.get(pk=product_id, is_active=True, is_deleted=False)
        comparison.products.add(product)
        return comparison

    @staticmethod
    def create_price_alert(user, product, target_price, variant=None):
        alert, created = PriceAlert.objects.update_or_create(
            user=user,
            product=product,
            variant=variant,
            defaults={
                "target_price": Decimal(str(target_price)),
                "is_active": True,
                "notified": False,
            },
        )
        return alert, created

    @staticmethod
    def check_price_alerts():
        alerts = PriceAlert.objects.filter(is_active=True, notified=False).select_related(
            "product", "variant", "user"
        )
        triggered = []
        for alert in alerts:
            current_price = alert.variant.price if alert.variant else alert.product.base_price
            if current_price <= alert.target_price:
                alert.notified = True
                alert.save(update_fields=["notified"])
                triggered.append(alert)
        return triggered
