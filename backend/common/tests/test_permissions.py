import pytest
from django.contrib.auth.models import AnonymousUser
from rest_framework.test import APIRequestFactory

from apps.accounts.models import User
from common.permissions import IsAdminRole

factory = APIRequestFactory()


def has_permission(user: User | AnonymousUser) -> bool:
    request = factory.get("/")
    request.user = user
    return IsAdminRole().has_permission(request, view=None)  # type: ignore[arg-type]


def test_anonymous_is_denied() -> None:
    assert not has_permission(AnonymousUser())


def test_regular_user_is_denied(user: User) -> None:
    assert not has_permission(user)


def test_admin_role_is_allowed(admin: User) -> None:
    assert has_permission(admin)


@pytest.mark.django_db
def test_staff_without_admin_role_is_denied() -> None:
    staff = User.objects.create_user(email="staff@example.com", is_staff=True)

    assert not has_permission(staff)
