from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.blog.models import BlogCategory, BlogComment, BlogPost
from apps.blog.serializers import (
    BlogCategorySerializer,
    BlogCommentSerializer,
    BlogPostDetailSerializer,
    BlogPostListSerializer,
)
from core.permissions.base import IsOwnerOrReadOnly
from core.utils.pagination import StandardResultsSetPagination


class BlogCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"
    search_fields = ["name", "name_fa"]


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True).select_related("author", "category")
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"
    filterset_fields = ["category"]
    search_fields = ["title", "title_fa", "excerpt", "content"]
    ordering_fields = ["published_at", "view_count"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=["view_count"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogCommentViewSet(viewsets.ModelViewSet):
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        queryset = BlogComment.objects.filter(is_approved=True, parent__isnull=True).select_related("user")
        post_slug = self.request.query_params.get("post")
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
        return queryset
