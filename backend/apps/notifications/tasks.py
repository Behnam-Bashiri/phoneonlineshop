from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template

from apps.notifications.models import Notification, NotificationTemplate


@shared_task
def send_notification(user_id, notification_type, title, message, title_fa="", message_fa="", link="", data=None):
    from apps.accounts.models import User

    user = User.objects.filter(id=user_id).first()
    if not user:
        return

    Notification.objects.create(
        user=user,
        notification_type=notification_type,
        title=title,
        title_fa=title_fa,
        message=message,
        message_fa=message_fa,
        link=link,
        data=data or {},
    )


@shared_task
def send_templated_notification(user_id, template_name, context=None):
    template = NotificationTemplate.objects.filter(name=template_name, is_active=True).first()
    if not template:
        return

    ctx = context or {}
    title = Template(template.title_template).render(Context(ctx))
    message = Template(template.message_template).render(Context(ctx))

    send_notification.delay(
        user_id,
        template.notification_type,
        title,
        message,
        link=ctx.get("link", ""),
        data=ctx,
    )

    if template.email_template:
        send_email_notification.delay(user_id, template.email_template, ctx)


@shared_task
def send_email_notification(user_id, subject_template, context=None):
    from apps.accounts.models import User

    user = User.objects.filter(id=user_id).first()
    if not user or not user.email:
        return

    ctx = context or {}
    if isinstance(subject_template, str) and "{{" in subject_template:
        subject = Template(subject_template).render(Context(ctx))
        body = ctx.get("body", subject)
    else:
        subject = str(subject_template)
        body = Template(subject_template).render(Context(ctx)) if "{{" in str(subject_template) else str(subject_template)

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


@shared_task
def send_password_reset_email(email, code):
    send_mail(
        subject="PhonyShop Password Reset",
        message=f"Your password reset code is: {code}\nThis code expires in 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )


@shared_task
def send_order_confirmation_email(user_id, order_number, total):
    send_templated_notification.delay(
        user_id,
        "order_confirmation",
        {"order_number": order_number, "total": str(total), "link": f"/orders/{order_number}"},
    )


@shared_task
def mark_notifications_read_bulk(user_id, notification_ids=None):
    queryset = Notification.objects.filter(user_id=user_id, is_read=False)
    if notification_ids:
        queryset = queryset.filter(id__in=notification_ids)
    return queryset.update(is_read=True)
