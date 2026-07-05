from django.conf import settings
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

from core.models import TimeStampedModel


class BlogCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(unique=True, max_length=120)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="blog/categories/", blank=True, null=True)

    class Meta:
        db_table = "blog_categories"
        verbose_name_plural = "blog categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(TimeStampedModel):
    title = models.CharField(max_length=255)
    title_fa = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, max_length=280)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="blog_posts")
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name="posts")
    excerpt = models.TextField(blank=True)
    content = RichTextField()
    content_fa = RichTextField(blank=True)
    featured_image = models.ImageField(upload_to="blog/posts/", blank=True, null=True)
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    reading_time_minutes = models.PositiveIntegerField(default=5)
    view_count = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = "blog_posts"
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogComment(TimeStampedModel):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    content = models.TextField()
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = "blog_comments"
        ordering = ["-created_at"]
