from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.models import (
    Address,
    LoginHistory,
    LoyaltyTransaction,
    UserAchievement,
    UserMembership,
    UserSession,
    Wallet,
    WalletTransaction,
)
from apps.accounts.serializers import (
    AddressSerializer,
    AchievementSerializer,
    ForgotPasswordSerializer,
    LoginHistorySerializer,
    LoginSerializer,
    LogoutSerializer,
    LoyaltyTransactionSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    UserAchievementSerializer,
    UserMembershipSerializer,
    UserSerializer,
    UserSessionSerializer,
    UserUpdateSerializer,
    WalletSerializer,
    WalletTransactionSerializer,
)
from apps.accounts.services import AuthService, OTPService, WalletService
from apps.notifications.tasks import send_password_reset_email
from core.permissions.base import IsOwnerOrReadOnly
from core.utils.pagination import StandardResultsSetPagination


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = AuthService.register_user(
                email=data["email"],
                password=data["password"],
                username=data.get("username") or None,
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                referral_code=data.get("referral_code") or None,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        tokens = AuthService.get_tokens_for_user(user)
        AuthService.record_login(user, request)
        return Response(
            {"user": UserSerializer(user).data, "tokens": tokens},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = AuthService.login_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                request=request,
            )
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = AuthService.get_tokens_for_user(user)
        AuthService.record_login(user, request)
        return Response({"user": UserSerializer(user).data, "tokens": tokens})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            AuthService.logout_user(serializer.validated_data["refresh"])
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = OTPService.request_password_reset(serializer.validated_data["email"])
        if otp:
            send_password_reset_email.delay(otp.identifier, otp.code)
        return Response(
            {"detail": "If the email exists, a reset code has been sent."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            OTPService.reset_password(data["email"], data["code"], data["new_password"])
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).select_related("province", "city")


class WalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return WalletService.get_or_create_wallet(self.request.user)


class WalletTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WalletTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        wallet = WalletService.get_or_create_wallet(self.request.user)
        return WalletTransaction.objects.filter(wallet=wallet)


class MembershipView(generics.RetrieveAPIView):
    serializer_class = UserMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserMembership.objects.select_related("level").get(user=self.request.user)


class LoyaltyTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoyaltyTransactionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return LoyaltyTransaction.objects.filter(user=self.request.user)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        from apps.accounts.models import Achievement

        return Achievement.objects.all()


class UserAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserAchievementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user).select_related("achievement")


class LoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoginHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)


class UserSessionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "delete", "head", "options"]

    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def revoke_all(self, request):
        updated = UserSession.objects.filter(user=request.user, is_active=True).update(is_active=False)
        return Response({"detail": f"{updated} sessions revoked."})
