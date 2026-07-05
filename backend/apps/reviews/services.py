from decimal import Decimal

from django.db.models import Avg, Count
from django.db import transaction

from apps.catalog.models import Product
from apps.reviews.models import ProductAnswer, ProductQuestion, Review, ReviewHelpful


class ReviewService:
    @staticmethod
    @transaction.atomic
    def create_review(user, product, rating, content, title="", pros=None, cons=None):
        if Review.objects.filter(user=user, product=product).exists():
            raise ValueError("You have already reviewed this product.")

        review = Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            title=title,
            content=content,
            pros=pros or [],
            cons=cons or [],
        )
        ReviewService.update_product_rating(product)
        return review

    @staticmethod
    def update_product_rating(product):
        stats = Review.objects.filter(product=product, is_approved=True).aggregate(
            avg_rating=Avg("rating"),
            count=Count("id"),
        )
        product.average_rating = Decimal(str(stats["avg_rating"] or 0)).quantize(Decimal("0.01"))
        product.review_count = stats["count"] or 0
        product.save(update_fields=["average_rating", "review_count"])

    @staticmethod
    @transaction.atomic
    def mark_helpful(review, user):
        vote, created = ReviewHelpful.objects.get_or_create(review=review, user=user)
        if created:
            review.helpful_count += 1
            review.save(update_fields=["helpful_count"])
        return created

    @staticmethod
    def create_question(user, product, question_text):
        return ProductQuestion.objects.create(user=user, product=product, question=question_text)

    @staticmethod
    def create_answer(user, question, answer_text, is_official=False):
        return ProductAnswer.objects.create(
            user=user,
            question=question,
            answer=answer_text,
            is_official=is_official,
        )
