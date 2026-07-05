from django.contrib import admin

from apps.accounts.models import (
    Achievement,
    Address,
    LoginHistory,
    LoyaltyTransaction,
    MembershipLevel,
    OTPVerification,
    Profile,
    User,
    UserAchievement,
    UserMembership,
    UserSession,
    Wallet,
    WalletTransaction,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "username", "first_name", "last_name", "is_active", "is_staff", "date_joined"]
    list_filter = ["is_active", "is_staff", "is_email_verified", "preferred_language"]
    search_fields = ["email", "username", "first_name", "last_name", "referral_code"]
    readonly_fields = ["id", "date_joined", "last_login", "referral_code"]
    ordering = ["-date_joined"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name_fa", "last_name_fa", "company"]
    search_fields = ["user__email", "first_name_fa", "last_name_fa", "national_id"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "recipient_name", "province", "city", "is_default"]
    list_filter = ["is_default", "province"]
    search_fields = ["user__email", "recipient_name", "postal_code", "address_line"]


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "balance", "bonus_balance", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["user__email"]


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ["wallet", "transaction_type", "amount", "status", "created_at"]
    list_filter = ["transaction_type", "status"]
    search_fields = ["wallet__user__email", "reference_id", "description"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(MembershipLevel)
class MembershipLevelAdmin(admin.ModelAdmin):
    list_display = ["name", "min_points", "cashback_percent", "discount_percent"]
    ordering = ["min_points"]


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "level", "points", "total_spent"]
    list_filter = ["level"]
    search_fields = ["user__email"]


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "points", "description", "created_at"]
    search_fields = ["user__email", "description"]
    list_filter = ["created_at"]


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "ip_address", "device", "is_successful", "created_at"]
    list_filter = ["is_successful", "device"]
    search_fields = ["user__email", "ip_address"]


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "ip_address", "is_active", "last_activity"]
    list_filter = ["is_active"]
    search_fields = ["user__email", "session_key"]


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ["identifier", "otp_type", "is_used", "expires_at", "created_at"]
    list_filter = ["otp_type", "is_used"]
    search_fields = ["identifier", "user__email"]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["name", "name_fa", "points_reward"]
    search_fields = ["name", "name_fa"]


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ["user", "achievement", "earned_at"]
    search_fields = ["user__email", "achievement__name"]
    list_filter = ["earned_at"]
