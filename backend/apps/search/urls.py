from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.search.views import (
    InstantSearchView,
    PopularSearchViewSet,
    SearchHistoryViewSet,
    SuggestionsView,
)

router = DefaultRouter()
router.register("history", SearchHistoryViewSet, basename="search-history")
router.register("popular", PopularSearchViewSet, basename="popular-search")

urlpatterns = [
    path("suggestions/", SuggestionsView.as_view(), name="search-suggestions"),
    path("", include(router.urls)),
    path("", InstantSearchView.as_view(), name="instant-search"),
]
