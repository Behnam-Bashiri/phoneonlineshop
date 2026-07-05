import random
import string

from django.db import transaction

from apps.support.models import SupportTicket, TicketReply


class SupportService:
    @staticmethod
    def generate_ticket_number():
        return f"TK{''.join(random.choices(string.digits, k=8))}"

    @classmethod
    @transaction.atomic
    def create_ticket(cls, user, department, subject, message, priority=None, order=None):
        ticket = SupportTicket.objects.create(
            ticket_number=cls.generate_ticket_number(),
            user=user,
            department=department,
            subject=subject,
            priority=priority or SupportTicket.Priority.MEDIUM,
            order=order,
        )
        TicketReply.objects.create(
            ticket=ticket,
            user=user,
            message=message,
            is_staff_reply=False,
        )
        return ticket

    @staticmethod
    @transaction.atomic
    def add_reply(ticket, user, message, is_internal=False):
        is_staff = user.is_staff
        reply = TicketReply.objects.create(
            ticket=ticket,
            user=user,
            message=message,
            is_internal=is_internal,
            is_staff_reply=is_staff,
        )
        if is_staff and ticket.status == SupportTicket.Status.OPEN:
            ticket.status = SupportTicket.Status.IN_PROGRESS
            ticket.save(update_fields=["status", "updated_at"])
        return reply
