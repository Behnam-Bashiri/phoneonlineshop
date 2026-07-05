from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.blog.views import BlogCategoryViewSet, BlogCommentViewSet, BlogPostViewSet

router = DefaultRouter()
router.register("categories", BlogCategoryViewSet, basename="blog-category")
router.register("posts", BlogPostViewSet, basename="blog-post")
router.register("comments", BlogCommentViewSet, basename="blog-comment")

urlpatterns = [
    path("", include(router.urls)),
]
