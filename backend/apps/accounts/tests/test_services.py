import pytest
from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.services import EMAIL_TAKEN_MESSAGE, register_user

pytestmark = pytest.mark.django_db

PASSWORD = "Str0ng-pass!"


def test_register_user_always_creates_role_user() -> None:
    user = register_user(email="ann@example.com", password=PASSWORD)

    assert user.role == User.Role.USER
    assert user.check_password(PASSWORD)


def test_concurrent_duplicate_becomes_validation_error() -> None:
    # Simulates the race: the serializer check is bypassed, the DB constraint
    # fires, and the service reports it like a normal validation error
    register_user(email="ann@example.com", password=PASSWORD)

    with pytest.raises(serializers.ValidationError) as exc_info:
        register_user(email="ann@example.com", password=PASSWORD)

    assert exc_info.value.detail == {"email": [EMAIL_TAKEN_MESSAGE]}
    assert User.objects.count() == 1
