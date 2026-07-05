from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Review(TimeStampedModel):
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    pros = models.JSONField(default=list, blank=True)
    cons = models.JSONField(default=list, blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False, db_index=True)
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "reviews"
        unique_together = ["product", "user"]
        ordering = ["-created_at"]


class ReviewImage(TimeStampedModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="reviews/")

    class Meta:
        db_table = "review_images"


class ReviewHelpful(TimeStampedModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="helpful_votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "review_helpful"
        unique_together = ["review", "user"]


class ProductQuestion(TimeStampedModel):
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE, related_name="questions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    is_approved = models.BooleanField(default=True)

    class Meta:
        db_table = "product_questions"
        ordering = ["-created_at"]


class ProductAnswer(TimeStampedModel):
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.TextField()
    is_official = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "product_answers"
        ordering = ["-is_official", "-helpful_count"]
