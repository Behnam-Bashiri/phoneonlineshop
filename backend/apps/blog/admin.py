from django.contrib import admin

from apps.blog.models import BlogCategory, BlogComment, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "name_fa", "slug"]
    search_fields = ["name", "name_fa", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "is_published", "published_at", "view_count"]
    list_filter = ["is_published", "category"]
    search_fields = ["title", "title_fa", "slug"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ["post", "user", "is_approved", "created_at"]
    list_filter = ["is_approved"]
    search_fields = ["content", "user__email", "post__title"]
