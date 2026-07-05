from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.reviews.models import ProductQuestion, Review
from apps.reviews.serializers import (
    ProductAnswerCreateSerializer,
    ProductAnswerSerializer,
    ProductQuestionSerializer,
    ReviewSerializer,
)
from apps.reviews.services import ReviewService
from core.permissions.base import IsOwnerOrReadOnly
from core.utils.pagination import StandardResultsSetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["product", "rating"]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return Review.objects.filter(is_approved=True).select_related("user", "product")

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def helpful(self, request, pk=None):
        review = self.get_object()
        created = ReviewService.mark_helpful(review, request.user)
        return Response({"detail": "Marked helpful." if created else "Already marked.", "helpful_count": review.helpful_count})


class ProductQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = ProductQuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ["product"]
    http_method_names = ["get", "post", "head", "options"]

    def get_queryset(self):
        return ProductQuestion.objects.filter(is_approved=True).select_related("user", "product").prefetch_related(
            "answers__user"
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def answer(self, request, pk=None):
        question = self.get_object()
        serializer = ProductAnswerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = ReviewService.create_answer(
            request.user,
            question,
            serializer.validated_data["answer"],
            is_official=request.user.is_staff,
        )
        return Response(ProductAnswerSerializer(answer).data, status=status.HTTP_201_CREATED)
