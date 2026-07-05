from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class TicketDepartment(TimeStampedModel):
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "ticket_departments"

    def __str__(self):
        return self.name


class SupportTicket(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        WAITING = "waiting", "Waiting for Customer"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    ticket_number = models.CharField(max_length=20, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")
    department = models.ForeignKey(TicketDepartment, on_delete=models.PROTECT, related_name="tickets")
    subject = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets"
    )

    class Meta:
        db_table = "support_tickets"
        ordering = ["-created_at"]


class TicketReply(TimeStampedModel):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal = models.BooleanField(default=False)
    is_staff_reply = models.BooleanField(default=False)

    class Meta:
        db_table = "ticket_replies"
        ordering = ["created_at"]
        verbose_name_plural = "ticket replies"


class TicketAttachment(TimeStampedModel):
    reply = models.ForeignKey(TicketReply, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="tickets/")
    filename = models.CharField(max_length=255)

    class Meta:
        db_table = "ticket_attachments"
