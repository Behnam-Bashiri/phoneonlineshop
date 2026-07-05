from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import (
    Achievement,
    Address,
    LoginHistory,
    LoyaltyTransaction,
    MembershipLevel,
    Profile,
    User,
    UserAchievement,
    UserMembership,
    UserSession,
    Wallet,
    WalletTransaction,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "first_name_fa",
            "last_name_fa",
            "national_id",
            "birth_date",
            "bio",
            "company",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "is_email_verified",
            "is_phone_verified",
            "preferred_language",
            "preferred_theme",
            "two_factor_enabled",
            "referral_code",
            "date_joined",
            "profile",
        ]
        read_only_fields = [
            "id",
            "is_email_verified",
            "is_phone_verified",
            "referral_code",
            "date_joined",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "preferred_language",
            "preferred_theme",
            "profile",
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        instance = super().update(instance, validated_data)
        if profile_data:
            profile, _ = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return instance


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True, default="")
    last_name = serializers.CharField(required=False, allow_blank=True, default="")
    referral_code = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class AddressSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source="province.name", read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = Address
        fields = [
            "id",
            "title",
            "recipient_name",
            "phone",
            "province",
            "city",
            "province_name",
            "city_name",
            "postal_code",
            "address_line",
            "is_default",
            "latitude",
            "longitude",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        if validated_data.get("is_default"):
            Address.objects.filter(user=validated_data["user"], is_default=True).update(is_default=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get("is_default"):
            Address.objects.filter(user=instance.user, is_default=True).exclude(pk=instance.pk).update(
                is_default=False
            )
        return super().update(instance, validated_data)


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["id", "balance", "bonus_balance", "is_active", "created_at", "updated_at"]
        read_only_fields = fields


class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "transaction_type",
            "amount",
            "balance_after",
            "status",
            "description",
            "reference_id",
            "order",
            "created_at",
        ]
        read_only_fields = fields


class MembershipLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipLevel
        fields = [
            "id",
            "name",
            "min_points",
            "cashback_percent",
            "discount_percent",
            "birthday_gift_amount",
            "icon",
            "color",
            "description",
        ]


class UserMembershipSerializer(serializers.ModelSerializer):
    level = MembershipLevelSerializer(read_only=True)

    class Meta:
        model = UserMembership
        fields = ["id", "level", "points", "total_spent", "created_at", "updated_at"]
        read_only_fields = fields


class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyTransaction
        fields = ["id", "points", "description", "order", "created_at"]
        read_only_fields = fields


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "name", "name_fa", "description", "icon", "points_reward", "criteria"]


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)

    class Meta:
        model = UserAchievement
        fields = ["id", "achievement", "earned_at"]
        read_only_fields = fields


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = [
            "id",
            "ip_address",
            "user_agent",
            "device",
            "location",
            "is_successful",
            "created_at",
        ]
        read_only_fields = fields


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = [
            "id",
            "session_key",
            "ip_address",
            "user_agent",
            "is_active",
            "last_activity",
            "created_at",
        ]
        read_only_fields = fields
