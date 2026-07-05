from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import (
    AchievementViewSet,
    AddressViewSet,
    ForgotPasswordView,
    LoginHistoryViewSet,
    LoginView,
    LogoutView,
    LoyaltyTransactionViewSet,
    MembershipView,
    ProfileView,
    RegisterView,
    ResetPasswordView,
    UserAchievementViewSet,
    UserSessionViewSet,
    WalletTransactionViewSet,
    WalletView,
)

router = DefaultRouter()
router.register("addresses", AddressViewSet, basename="address")
router.register("wallet/transactions", WalletTransactionViewSet, basename="wallet-transaction")
router.register("membership/loyalty", LoyaltyTransactionViewSet, basename="loyalty-transaction")
router.register("achievements", AchievementViewSet, basename="achievement")
router.register("my-achievements", UserAchievementViewSet, basename="user-achievement")
router.register("sessions", UserSessionViewSet, basename="session")
router.register("login-history", LoginHistoryViewSet, basename="login-history")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("wallet/", WalletView.as_view(), name="wallet"),
    path("membership/", MembershipView.as_view(), name="membership"),
    path("", include(router.urls)),
]
