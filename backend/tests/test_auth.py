import pytest
from rest_framework import status


@pytest.mark.django_db
class TestAuthAPI:
    def test_register(self, api_client):
        response = api_client.post(
            "/api/v1/auth/register/",
            {
                "email": "newuser@example.com",
                "password": "SecurePass123!",
                "first_name": "New",
                "last_name": "User",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "tokens" in response.data
        assert "access" in response.data["tokens"]
        assert response.data["user"]["email"] == "newuser@example.com"

    def test_register_duplicate_email(self, api_client, user):
        response = api_client.post(
            "/api/v1/auth/register/",
            {"email": user.email, "password": "SecurePass123!"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login(self, api_client, user):
        response = api_client.post(
            "/api/v1/auth/login/",
            {"email": user.email, "password": "TestPass123!"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "tokens" in response.data

    def test_login_invalid_credentials(self, api_client, user):
        response = api_client.post(
            "/api/v1/auth/login/",
            {"email": user.email, "password": "wrongpassword"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_profile_authenticated(self, authenticated_client, user):
        response = authenticated_client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_profile_unauthenticated(self, api_client):
        response = api_client.get("/api/v1/auth/profile/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_wallet_created_on_register(self, api_client):
        api_client.post(
            "/api/v1/auth/register/",
            {"email": "wallet@example.com", "password": "SecurePass123!"},
            format="json",
        )
        from apps.accounts.models import User, Wallet

        user = User.objects.get(email="wallet@example.com")
        assert Wallet.objects.filter(user=user).exists()

    def test_referral_code_generated(self, api_client):
        api_client.post(
            "/api/v1/auth/register/",
            {"email": "referral@example.com", "password": "SecurePass123!"},
            format="json",
        )
        from apps.accounts.models import User

        user = User.objects.get(email="referral@example.com")
        assert len(user.referral_code) > 0

    def test_forgot_password(self, api_client, user):
        response = api_client.post(
            "/api/v1/auth/forgot-password/",
            {"email": user.email},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_token_refresh(self, api_client, user):
        login_response = api_client.post(
            "/api/v1/auth/login/",
            {"email": user.email, "password": "TestPass123!"},
            format="json",
        )
        refresh_token = login_response.data["tokens"]["refresh"]
        response = api_client.post(
            "/api/v1/auth/refresh/",
            {"refresh": refresh_token},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
