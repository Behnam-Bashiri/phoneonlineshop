from django.contrib import admin

from apps.support.models import SupportTicket, TicketAttachment, TicketDepartment, TicketReply


@admin.register(TicketDepartment)
class TicketDepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "name_fa", "email", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "name_fa"]


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0
    readonly_fields = ["user", "message", "is_staff_reply", "created_at"]


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ["ticket_number", "user", "department", "priority", "status", "created_at"]
    list_filter = ["status", "priority", "department"]
    search_fields = ["ticket_number", "subject", "user__email"]
    inlines = [TicketReplyInline]


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ["ticket", "user", "is_staff_reply", "is_internal", "created_at"]
    list_filter = ["is_staff_reply", "is_internal"]


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ["reply", "filename", "created_at"]
