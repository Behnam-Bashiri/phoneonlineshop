from django.contrib import admin

from apps.reviews.models import ProductAnswer, ProductQuestion, Review, ReviewHelpful, ReviewImage


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating", "is_approved", "helpful_count", "created_at"]
    list_filter = ["is_approved", "rating"]
    search_fields = ["product__name", "user__email", "content"]
    inlines = [ReviewImageInline]


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ["review", "user", "created_at"]


@admin.register(ProductQuestion)
class ProductQuestionAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "is_approved", "created_at"]
    list_filter = ["is_approved"]
    search_fields = ["question", "product__name"]


@admin.register(ProductAnswer)
class ProductAnswerAdmin(admin.ModelAdmin):
    list_display = ["question", "user", "is_official", "is_approved", "helpful_count"]
    list_filter = ["is_official", "is_approved"]
