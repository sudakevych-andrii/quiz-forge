from typing import Any

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.throttling import ScopedRateThrottle

from apps.accounts.models import User

pytestmark = pytest.mark.django_db

URL = reverse("register")
PASSWORD = "Str0ng-pass!"


def register(client: APIClient, **overrides: Any) -> Any:
    payload = {"email": "ann@example.com", "password": PASSWORD, **overrides}
    return client.post(URL, payload, format="json")


def test_register_creates_regular_user(api_client: APIClient) -> None:
    response = register(api_client, email="Ann@Example.com", first_name="Ann")

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "ann@example.com"
    assert body["first_name"] == "Ann"
    assert body["role"] == "USER"
    assert "password" not in body

    user = User.objects.get(email="ann@example.com")
    assert str(user.id) == body["id"]
    assert user.check_password(PASSWORD)
    assert not user.is_staff


def test_role_from_payload_is_ignored(api_client: APIClient) -> None:
    response = register(api_client, role="ADMIN", is_staff=True, is_superuser=True)

    assert response.status_code == 201
    user = User.objects.get(email="ann@example.com")
    assert user.role == User.Role.USER
    assert not user.is_staff
    assert not user.is_superuser


def test_duplicate_email_is_rejected_regardless_of_case(
    api_client: APIClient,
) -> None:
    register(api_client)

    response = register(api_client, email="ANN@example.com")

    assert response.status_code == 400
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["details"] == {"email": ["A user with this email already exists."]}


@pytest.mark.parametrize(
    ("password", "message_part"),
    [
        ("Sh0rt!", "too short"),
        ("password123", "too common"),
        ("4815162342", "entirely numeric"),
        ("ann@example.com", "too similar"),
    ],
)
def test_weak_password_is_rejected(
    api_client: APIClient, password: str, message_part: str
) -> None:
    response = register(api_client, password=password)

    assert response.status_code == 400
    messages = response.json()["error"]["details"]["password"]
    assert any(message_part in m for m in messages)
    assert not User.objects.exists()


@pytest.mark.parametrize("field", ["email", "password"])
def test_required_fields(api_client: APIClient, field: str) -> None:
    payload = {"email": "ann@example.com", "password": PASSWORD}
    del payload[field]

    response = api_client.post(URL, payload, format="json")

    assert response.status_code == 400
    assert field in response.json()["error"]["details"]


def test_register_is_throttled(
    api_client: APIClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(ScopedRateThrottle, "THROTTLE_RATES", {"register": "2/hour"})

    register(api_client, email="a@example.com")
    register(api_client, email="b@example.com")
    response = register(api_client, email="c@example.com")

    assert response.status_code == 429
    assert response.json()["error"]["code"] == "THROTTLED"
    assert "Retry-After" in response
