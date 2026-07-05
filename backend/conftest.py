import os
from decimal import Decimal

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

if not settings.configured:
    django.setup()

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    from apps.accounts.models import User

    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPass123!",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
