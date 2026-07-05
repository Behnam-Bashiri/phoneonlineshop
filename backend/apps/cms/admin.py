from django.contrib import admin

from apps.cms.models import (
    Banner,
    CustomerReview,
    FAQ,
    InstagramPost,
    LandingPage,
    LandingSection,
    Menu,
    MenuItem,
    NewsletterSubscriber,
    Page,
    Partner,
    SiteSettings,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ["site_name", "phone", "email", "maintenance_mode"]


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "is_active"]
    list_filter = ["location", "is_active"]
    inlines = [MenuItemInline]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "is_published", "sort_order"]
    list_filter = ["is_published"]
    search_fields = ["title", "title_fa", "slug"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "location", "is_active", "sort_order"]
    list_filter = ["location", "is_active"]


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "category", "is_active", "sort_order"]
    list_filter = ["category", "is_active"]
    search_fields = ["question", "question_fa"]


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ["email", "is_active", "confirmed_at", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["email"]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "sort_order"]
    list_filter = ["is_active"]


@admin.register(InstagramPost)
class InstagramPostAdmin(admin.ModelAdmin):
    list_display = ["caption", "is_active", "sort_order"]
    list_filter = ["is_active"]


class LandingSectionInline(admin.TabularInline):
    model = LandingSection
    extra = 1


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "is_published"]
    list_filter = ["is_published"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LandingSectionInline]


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ["author_name", "rating", "is_featured", "is_active"]
    list_filter = ["is_featured", "is_active"]
    search_fields = ["author_name", "content"]
