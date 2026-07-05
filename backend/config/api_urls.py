from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.accounts.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("cart/", include("apps.cart.urls")),
    path("orders/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
    path("blog/", include("apps.blog.urls")),
    path("cms/", include("apps.cms.urls")),
    path("support/", include("apps.support.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("promotions/", include("apps.promotions.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("search/", include("apps.search.urls")),
    path("analytics/", include("apps.analytics.urls")),
]
