from django.db.models import Q
from django_filters import rest_framework as filters

from apps.catalog.models import Product


class ProductFilter(filters.FilterSet):
    brand = filters.NumberFilter(field_name="brand_id")
    category = filters.NumberFilter(field_name="category_id")
    min_price = filters.NumberFilter(field_name="base_price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="base_price", lookup_expr="lte")
    is_featured = filters.BooleanFilter()
    is_new_arrival = filters.BooleanFilter()
    is_best_seller = filters.BooleanFilter()
    in_stock = filters.BooleanFilter(method="filter_in_stock")
    tags = filters.CharFilter(method="filter_tags")

    class Meta:
        model = Product
        fields = [
            "brand",
            "category",
            "is_active",
            "is_featured",
            "is_new_arrival",
            "is_best_seller",
        ]

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(variants__stock_quantity__gt=0, variants__is_active=True).distinct()
        return queryset.filter(
            Q(variants__stock_quantity=0) | Q(variants__isnull=True)
        ).distinct()

    def filter_tags(self, queryset, name, value):
        tags = [tag.strip() for tag in value.split(",") if tag.strip()]
        for tag in tags:
            queryset = queryset.filter(tags__name__iexact=tag)
        return queryset.distinct()
