"""Fixtures shared by all tests."""

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User

PASSWORD = "Str0ng-pass!"


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db: None) -> User:
    return User.objects.create_user(email="user@example.com", password=PASSWORD)


@pytest.fixture
def admin(db: None) -> User:
    return User.objects.create_superuser(email="admin@example.com", password=PASSWORD)
