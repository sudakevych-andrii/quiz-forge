"""Fixtures shared by all tests."""

import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from apps.accounts.models import User

PASSWORD = "Str0ng-pass!"


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    """Throttling counters live in the cache; don't leak them between tests."""
    cache.clear()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db: None) -> User:
    return User.objects.create_user(email="user@example.com", password=PASSWORD)


@pytest.fixture
def admin(db: None) -> User:
    return User.objects.create_superuser(email="admin@example.com", password=PASSWORD)
