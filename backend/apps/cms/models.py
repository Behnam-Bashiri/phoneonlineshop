from django.conf import settings
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

from core.models import TimeStampedModel


class SiteSettings(TimeStampedModel):
    site_name = models.CharField(max_length=100, default="PhonyShop")
    site_name_fa = models.CharField(max_length=100, default="فونی‌شاپ")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    logo_dark = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    address_fa = models.TextField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_telegram = models.URLField(blank=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=9)
    currency = models.CharField(max_length=3, default="IRR")
    currency_symbol = models.CharField(max_length=10, default="تومان")
    free_shipping_threshold = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    maintenance_mode = models.BooleanField(default=False)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    default_meta_title = models.CharField(max_length=200, blank=True)
    default_meta_description = models.TextField(blank=True)

    class Meta:
        db_table = "site_settings"
        verbose_name_plural = "site settings"

    def __str__(self):
        return self.site_name


class Page(TimeStampedModel):
    title = models.CharField(max_length=255)
    title_fa = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=280)
    content = RichTextField()
    content_fa = RichTextField(blank=True)
    is_published = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "pages"
        ordering = ["sort_order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Menu(TimeStampedModel):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50, choices=[
        ("header", "Header"), ("footer", "Footer"), ("mobile", "Mobile")
    ])
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "menus"


class MenuItem(TimeStampedModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="items")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    title = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=500, blank=True)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey("catalog.Category", on_delete=models.SET_NULL, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        db_table = "menu_items"
        ordering = ["sort_order"]


class Banner(TimeStampedModel):
    title = models.CharField(max_length=200)
    title_fa = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="banners/")
    image_mobile = models.ImageField(upload_to="banners/mobile/", blank=True, null=True)
    link_url = models.CharField(max_length=500, blank=True)
    button_text = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, default="home_hero")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "banners"
        ordering = ["sort_order"]


class FAQ(TimeStampedModel):
    question = models.CharField(max_length=500)
    question_fa = models.CharField(max_length=500, blank=True)
    answer = models.TextField()
    answer_fa = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "faqs"
        ordering = ["sort_order"]
        verbose_name = "FAQ"


class NewsletterSubscriber(TimeStampedModel):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "newsletter_subscribers"


class Partner(TimeStampedModel):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="partners/")
    website = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "partners"
        ordering = ["sort_order"]


class InstagramPost(TimeStampedModel):
    image = models.ImageField(upload_to="instagram/")
    caption = models.CharField(max_length=500, blank=True)
    link_url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "instagram_posts"
        ordering = ["sort_order"]


class LandingPage(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=280)
    is_published = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    class Meta:
        db_table = "landing_pages"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class LandingSection(TimeStampedModel):
    class SectionType(models.TextChoices):
        HERO = "hero", "Hero"
        BANNER = "banner", "Banner"
        PRODUCTS = "products", "Products"
        TEXT = "text", "Text"
        FAQ = "faq", "FAQ"
        GALLERY = "gallery", "Gallery"
        COUNTDOWN = "countdown", "Countdown"
        CTA = "cta", "Call to Action"
        STATS = "stats", "Statistics"

    page = models.ForeignKey(LandingPage, on_delete=models.CASCADE, related_name="sections")
    section_type = models.CharField(max_length=20, choices=SectionType.choices)
    title = models.CharField(max_length=255, blank=True)
    content = models.JSONField(default=dict)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "landing_sections"
        ordering = ["sort_order"]


class CustomerReview(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    content_fa = models.TextField(blank=True)
    rating = models.PositiveIntegerField(default=5)
    avatar = models.ImageField(upload_to="reviews/", blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "customer_reviews"
        ordering = ["sort_order"]
