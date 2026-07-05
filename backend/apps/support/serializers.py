from rest_framework import serializers

from apps.accounts.serializers import UserSerializer
from apps.support.models import SupportTicket, TicketAttachment, TicketDepartment, TicketReply


class TicketDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketDepartment
        fields = ["id", "name", "name_fa", "email", "is_active"]


class TicketAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ["id", "file", "filename", "created_at"]
        read_only_fields = fields


class TicketReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = TicketReply
        fields = [
            "id",
            "user",
            "message",
            "is_internal",
            "is_staff_reply",
            "attachments",
            "created_at",
        ]
        read_only_fields = ["id", "user", "is_staff_reply", "created_at"]


class SupportTicketListSerializer(serializers.ModelSerializer):
    department = TicketDepartmentSerializer(read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            "id",
            "ticket_number",
            "department",
            "subject",
            "priority",
            "status",
            "created_at",
        ]


class SupportTicketDetailSerializer(SupportTicketListSerializer):
    replies = serializers.SerializerMethodField()

    class Meta(SupportTicketListSerializer.Meta):
        fields = SupportTicketListSerializer.Meta.fields + ["order", "assigned_to", "replies", "updated_at"]

    def get_replies(self, obj):
        replies = obj.replies.all()
        if not self.context["request"].user.is_staff:
            replies = replies.filter(is_internal=False)
        return TicketReplySerializer(replies, many=True, context=self.context).data


class CreateTicketSerializer(serializers.Serializer):
    department_id = serializers.IntegerField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    priority = serializers.ChoiceField(
        choices=SupportTicket.Priority.choices,
        required=False,
        default=SupportTicket.Priority.MEDIUM,
    )
    order_id = serializers.UUIDField(required=False, allow_null=True)


class TicketReplyCreateSerializer(serializers.Serializer):
    message = serializers.CharField()
