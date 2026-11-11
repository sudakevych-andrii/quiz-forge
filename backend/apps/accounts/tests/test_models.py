import pytest
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.test import override_settings

from apps.accounts.models import User
from config.settings import base as base_settings

pytestmark = pytest.mark.django_db

PASSWORD = "Str0ng-pass!"


def test_create_user_normalizes_email_and_defaults_to_user_role() -> None:
    user = User.objects.create_user(email="  Ann@Example.COM ", password=PASSWORD)

    assert user.email == "ann@example.com"
    assert user.role == User.Role.USER
    assert not user.is_admin
    assert not user.is_staff
    assert not user.is_superuser
    assert user.check_password(PASSWORD)


def test_create_user_requires_email() -> None:
    with pytest.raises(ValueError, match="email must be set"):
        User.objects.create_user(email="", password=PASSWORD)


def test_email_is_unique_regardless_of_case() -> None:
    User.objects.create_user(email="ann@example.com", password=PASSWORD)

    with pytest.raises(IntegrityError):
        User.objects.create_user(email="ANN@example.com", password=PASSWORD)


def test_login_is_case_insensitive() -> None:
    User.objects.create_user(email="ann@example.com", password=PASSWORD)

    assert authenticate(username="ANN@Example.com", password=PASSWORD) is not None


def test_create_superuser_gets_admin_role() -> None:
    admin = User.objects.create_superuser(email="root@example.com", password=PASSWORD)

    assert admin.role == User.Role.ADMIN
    assert admin.is_admin
    assert admin.is_staff
    assert admin.is_superuser


@pytest.mark.parametrize("flag", ["is_staff", "is_superuser"])
def test_create_superuser_rejects_disabled_flags(flag: str) -> None:
    with pytest.raises(ValueError, match=flag):
        User.objects.create_superuser(
            email="root@example.com", password=PASSWORD, **{flag: False}
        )


def test_passwords_are_hashed_with_argon2id() -> None:
    # Test settings use a fast hasher; check the real configuration here
    with override_settings(PASSWORD_HASHERS=base_settings.PASSWORD_HASHERS):
        user = User.objects.create_user(email="ann@example.com", password=PASSWORD)

    assert user.password.startswith("argon2$argon2id$")


def test_str_is_email() -> None:
    user = User(email="ann@example.com")

    assert str(user) == "ann@example.com"
