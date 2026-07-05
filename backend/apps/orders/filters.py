import django_filters

from apps.orders.models import Order


class OrderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Order.Status.choices)
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    min_total = django_filters.NumberFilter(field_name="total", lookup_expr="gte")
    max_total = django_filters.NumberFilter(field_name="total", lookup_expr="lte")

    class Meta:
        model = Order
        fields = ["status", "shipping_method"]
