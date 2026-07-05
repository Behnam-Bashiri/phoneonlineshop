from decimal import Decimal

import pytest
from rest_framework import status

from apps.catalog.models import Brand, Category, Color, Product, ProductVariant, StorageOption


@pytest.fixture
def catalog_data(db):
    brand = Brand.objects.create(name="Apple", name_fa="اپل", slug="apple")
    category = Category.objects.create(name="Smartphones", name_fa="گوشی هوشمند", slug="smartphones")
    color = Color.objects.create(name="Black", name_fa="مشکی", hex_code="#000000")
    storage = StorageOption.objects.create(capacity="256GB", capacity_gb=256)
    product = Product.objects.create(
        name="iPhone 15 Pro",
        name_fa="آیفون ۱۵ پرو",
        slug="iphone-15-pro",
        sku="IP15P-001",
        brand=brand,
        category=category,
        description="Latest iPhone",
        base_price=Decimal("45000000"),
        compare_price=Decimal("48000000"),
        is_active=True,
        is_featured=True,
    )
    variant = ProductVariant.objects.create(
        product=product,
        sku="IP15P-001-BLK-256",
        color=color,
        storage=storage,
        price=Decimal("45000000"),
        stock_quantity=50,
        is_default=True,
    )
    return {
        "brand": brand,
        "category": category,
        "product": product,
        "variant": variant,
    }


@pytest.mark.django_db
class TestCatalogAPI:
    def test_list_products(self, api_client, catalog_data):
        response = api_client.get("/api/v1/catalog/products/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_product_detail(self, api_client, catalog_data):
        product = catalog_data["product"]
        response = api_client.get(f"/api/v1/catalog/products/{product.slug}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == product.name
        assert response.data["view_count"] >= 1

    def test_filter_products_by_brand(self, api_client, catalog_data):
        brand = catalog_data["brand"]
        response = api_client.get(f"/api/v1/catalog/products/?brand={brand.id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_search_products(self, api_client, catalog_data):
        response = api_client.get("/api/v1/catalog/products/?search=iPhone")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_list_brands(self, api_client, catalog_data):
        response = api_client.get("/api/v1/catalog/brands/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_list_categories(self, api_client, catalog_data):
        response = api_client.get("/api/v1/catalog/categories/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1

    def test_wishlist_add(self, authenticated_client, catalog_data):
        product = catalog_data["product"]
        response = authenticated_client.post(
            "/api/v1/catalog/wishlist/",
            {"product_id": product.id},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_wishlist_requires_auth(self, api_client, catalog_data):
        response = api_client.get("/api/v1/catalog/wishlist/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_price_alert_create(self, authenticated_client, catalog_data):
        product = catalog_data["product"]
        response = authenticated_client.post(
            "/api/v1/catalog/price-alerts/",
            {"product": product.id, "target_price": "40000000"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_instant_search(self, api_client, catalog_data):
        response = api_client.get("/api/v1/search/?q=iPhone")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1
