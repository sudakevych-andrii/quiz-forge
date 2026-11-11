from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import User

EMAIL_TAKEN_MESSAGE = "A user with this email already exists."


def register_user(
    *, email: str, password: str, first_name: str = "", last_name: str = ""
) -> User:
    """Create a regular user. The role is always USER: never taken from input."""
    try:
        with transaction.atomic():
            return User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.USER,
            )
    except IntegrityError as exc:
        # Two concurrent sign-ups with the same email: the serializer check
        # passed for both, the unique constraint stopped the second one
        raise serializers.ValidationError({"email": [EMAIL_TAKEN_MESSAGE]}) from exc
