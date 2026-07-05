import random
import string
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import (
    LoginHistory,
    OTPVerification,
    User,
    UserSession,
    Wallet,
    WalletTransaction,
)


class AuthService:
    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def register_user(email, password, username=None, first_name="", last_name="", referral_code=None):
        if User.objects.filter(email=email).exists():
            raise ValueError("A user with this email already exists.")

        if not username:
            username = email.split("@")[0]
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

        referred_by = None
        if referral_code:
            referred_by = User.objects.filter(referral_code=referral_code).first()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            referred_by=referred_by,
        )
        return user

    @staticmethod
    def login_user(email, password, request=None):
        user = authenticate(request=request, username=email, password=password)
        if user is None:
            raise ValueError("Invalid email or password.")
        if not user.is_active:
            raise ValueError("User account is disabled.")
        return user

    @staticmethod
    def logout_user(refresh_token):
        token = RefreshToken(refresh_token)
        token.blacklist()

    @staticmethod
    def record_login(user, request, is_successful=True):
        ip_address = AuthService._get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        device = AuthService._parse_device(user_agent)
        LoginHistory.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            device=device,
            is_successful=is_successful,
        )
        if is_successful:
            UserSession.objects.update_or_create(
                user=user,
                session_key=request.session.session_key or f"jwt-{user.id}",
                defaults={
                    "ip_address": ip_address,
                    "user_agent": user_agent,
                    "is_active": True,
                },
            )

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "127.0.0.1")

    @staticmethod
    def _parse_device(user_agent):
        ua_lower = user_agent.lower()
        if "mobile" in ua_lower or "android" in ua_lower or "iphone" in ua_lower:
            return "mobile"
        if "tablet" in ua_lower or "ipad" in ua_lower:
            return "tablet"
        return "desktop"


class OTPService:
    OTP_EXPIRY_MINUTES = 10

    @staticmethod
    def generate_code():
        return "".join(random.choices(string.digits, k=6))

    @classmethod
    def create_otp(cls, identifier, otp_type, user=None):
        code = cls.generate_code()
        expires_at = timezone.now() + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)
        OTPVerification.objects.filter(
            identifier=identifier,
            otp_type=otp_type,
            is_used=False,
        ).update(is_used=True)
        return OTPVerification.objects.create(
            user=user,
            identifier=identifier,
            otp_type=otp_type,
            code=code,
            expires_at=expires_at,
        )

    @classmethod
    def verify_otp(cls, identifier, otp_type, code):
        otp = (
            OTPVerification.objects.filter(
                identifier=identifier,
                otp_type=otp_type,
                code=code,
                is_used=False,
                expires_at__gt=timezone.now(),
            )
            .order_by("-created_at")
            .first()
        )
        if not otp:
            return None
        otp.is_used = True
        otp.save(update_fields=["is_used"])
        return otp

    @classmethod
    def request_password_reset(cls, email):
        user = User.objects.filter(email=email).first()
        if not user:
            return None
        return cls.create_otp(email, OTPVerification.OTPType.PASSWORD_RESET, user=user)

    @classmethod
    def reset_password(cls, email, code, new_password):
        otp = cls.verify_otp(email, OTPVerification.OTPType.PASSWORD_RESET, code)
        if not otp or not otp.user:
            raise ValueError("Invalid or expired reset code.")
        user = otp.user
        user.set_password(new_password)
        user.save(update_fields=["password"])
        return user


class WalletService:
    @staticmethod
    def get_or_create_wallet(user):
        wallet, _ = Wallet.objects.get_or_create(user=user)
        return wallet

    @staticmethod
    @transaction.atomic
    def deposit(wallet, amount, description="", reference_id=""):
        wallet.balance += amount
        wallet.save(update_fields=["balance", "updated_at"])
        return WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TransactionType.DEPOSIT,
            amount=amount,
            balance_after=wallet.balance,
            status=WalletTransaction.Status.COMPLETED,
            description=description,
            reference_id=reference_id,
        )

    @staticmethod
    @transaction.atomic
    def withdraw(wallet, amount, description="", reference_id="", order=None):
        if wallet.balance < amount:
            raise ValueError("Insufficient wallet balance.")
        wallet.balance -= amount
        wallet.save(update_fields=["balance", "updated_at"])
        return WalletTransaction.objects.create(
            wallet=wallet,
            transaction_type=WalletTransaction.TransactionType.WITHDRAW,
            amount=amount,
            balance_after=wallet.balance,
            status=WalletTransaction.Status.COMPLETED,
            description=description,
            reference_id=reference_id,
            order=order,
        )
