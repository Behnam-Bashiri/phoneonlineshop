import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedModel


class User(AbstractUser):
    """Custom user model with email/phone authentication."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    phone = PhoneNumberField(blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    preferred_language = models.CharField(max_length=5, default="en", choices=[("en", "English"), ("fa", "Persian")])
    preferred_theme = models.CharField(max_length=10, default="system", choices=[("light", "Light"), ("dark", "Dark"), ("system", "System")])
    two_factor_enabled = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=20, unique=True, blank=True)
    referred_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="referrals")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["referral_code"]),
        ]

    def __str__(self):
        return self.email


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name_fa = models.CharField(max_length=100, blank=True)
    last_name_fa = models.CharField(max_length=100, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    company = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "profiles"


class Address(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    title = models.CharField(max_length=100)
    recipient_name = models.CharField(max_length=200)
    phone = PhoneNumberField()
    province = models.ForeignKey("orders.Province", on_delete=models.PROTECT, related_name="addresses")
    city = models.ForeignKey("orders.City", on_delete=models.PROTECT, related_name="addresses")
    postal_code = models.CharField(max_length=20)
    address_line = models.TextField()
    is_default = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    class Meta:
        db_table = "addresses"
        verbose_name_plural = "addresses"


class Wallet(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    bonus_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "wallets"


class WalletTransaction(TimeStampedModel):
    class TransactionType(models.TextChoices):
        DEPOSIT = "deposit", "Deposit"
        WITHDRAW = "withdraw", "Withdraw"
        PURCHASE = "purchase", "Purchase"
        REFUND = "refund", "Refund"
        CASHBACK = "cashback", "Cashback"
        BONUS = "bonus", "Bonus"
        REFERRAL = "referral", "Referral"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    balance_after = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.COMPLETED)
    description = models.TextField(blank=True)
    reference_id = models.CharField(max_length=100, blank=True, db_index=True)
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "wallet_transactions"
        ordering = ["-created_at"]


class MembershipLevel(TimeStampedModel):
    class Level(models.TextChoices):
        BRONZE = "bronze", "Bronze"
        SILVER = "silver", "Silver"
        GOLD = "gold", "Gold"
        DIAMOND = "diamond", "Diamond"
        VIP = "vip", "VIP"

    name = models.CharField(max_length=20, choices=Level.choices, unique=True)
    min_points = models.PositiveIntegerField(default=0)
    cashback_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    birthday_gift_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    icon = models.ImageField(upload_to="membership/", blank=True, null=True)
    color = models.CharField(max_length=7, default="#CD7F32")
    description = models.TextField(blank=True)

    class Meta:
        db_table = "membership_levels"
        ordering = ["min_points"]


class UserMembership(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="membership")
    level = models.ForeignKey(MembershipLevel, on_delete=models.PROTECT, related_name="members")
    points = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        db_table = "user_memberships"


class LoyaltyTransaction(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loyalty_transactions")
    points = models.IntegerField()
    description = models.CharField(max_length=255)
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "loyalty_transactions"
        ordering = ["-created_at"]


class LoginHistory(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="login_history")
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    device = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_successful = models.BooleanField(default=True)

    class Meta:
        db_table = "login_history"
        ordering = ["-created_at"]
        verbose_name_plural = "login histories"


class UserSession(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    session_key = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_sessions"


class OTPVerification(TimeStampedModel):
    class OTPType(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"
        PASSWORD_RESET = "password_reset", "Password Reset"
        TWO_FACTOR = "two_factor", "Two Factor"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps", null=True, blank=True)
    identifier = models.CharField(max_length=255)
    otp_type = models.CharField(max_length=20, choices=OTPType.choices)
    code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = "otp_verifications"


class Achievement(TimeStampedModel):
    name = models.CharField(max_length=100)
    name_fa = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to="achievements/", blank=True, null=True)
    points_reward = models.PositiveIntegerField(default=0)
    criteria = models.JSONField(default=dict)

    class Meta:
        db_table = "achievements"


class UserAchievement(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_achievements"
        unique_together = ["user", "achievement"]
