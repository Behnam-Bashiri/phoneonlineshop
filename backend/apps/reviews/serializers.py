from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.reviews.models import ProductAnswer, ProductQuestion, Review, ReviewImage


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["id", "image"]
        read_only_fields = fields


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "rating",
            "title",
            "content",
            "pros",
            "cons",
            "is_verified_purchase",
            "helpful_count",
            "images",
            "created_at",
        ]
        read_only_fields = ["id", "user", "is_verified_purchase", "helpful_count", "created_at"]

    def create(self, validated_data):
        from apps.reviews.services import ReviewService

        return ReviewService.create_review(
            user=self.context["request"].user,
            product=validated_data["product"],
            rating=validated_data["rating"],
            content=validated_data["content"],
            title=validated_data.get("title", ""),
            pros=validated_data.get("pros"),
            cons=validated_data.get("cons"),
        )


class ProductAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductAnswer
        fields = [
            "id",
            "user",
            "answer",
            "is_official",
            "helpful_count",
            "created_at",
        ]
        read_only_fields = ["id", "user", "helpful_count", "created_at"]


class ProductQuestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    answers = ProductAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ProductQuestion
        fields = ["id", "product", "user", "question", "answers", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def create(self, validated_data):
        from apps.reviews.services import ReviewService

        return ReviewService.create_question(
            user=self.context["request"].user,
            product=validated_data["product"],
            question_text=validated_data["question"],
        )


class ProductAnswerCreateSerializer(serializers.Serializer):
    answer = serializers.CharField()
