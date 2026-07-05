from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.reviews.views import ProductQuestionViewSet, ReviewViewSet

router = DefaultRouter()
router.register("reviews", ReviewViewSet, basename="review")
router.register("questions", ProductQuestionViewSet, basename="product-question")

urlpatterns = [
    path("", include(router.urls)),
]
