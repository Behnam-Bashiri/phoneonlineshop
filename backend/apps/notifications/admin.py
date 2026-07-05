from django.contrib import admin

from apps.notifications.models import Notification, NotificationTemplate


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "notification_type", "title", "is_read", "created_at"]
    list_filter = ["notification_type", "is_read"]
    search_fields = ["user__email", "title", "message"]


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ["name", "notification_type", "is_active"]
    list_filter = ["notification_type", "is_active"]
    search_fields = ["name"]
