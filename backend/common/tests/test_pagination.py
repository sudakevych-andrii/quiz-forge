import pytest
from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny
from rest_framework.test import APIRequestFactory

from apps.accounts.models import User

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class UserListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.order_by("email")
    serializer_class = UserEmailSerializer


@pytest.fixture
def three_users() -> None:
    for i in range(3):
        User.objects.create_user(email=f"u{i}@example.com", password="x")


def test_paginated_response_shape(three_users: None) -> None:
    response = UserListView.as_view()(factory.get("/", {"page": 2, "page_size": 2}))

    assert response.status_code == 200
    assert response.data == {
        "count": 3,
        "page": 2,
        "page_size": 2,
        "total_pages": 2,
        "results": [{"email": "u2@example.com"}],
    }


def test_page_size_is_capped(three_users: None) -> None:
    response = UserListView.as_view()(factory.get("/", {"page_size": 1000}))

    assert response.data["page_size"] == 100


def test_page_out_of_range_returns_404(three_users: None) -> None:
    response = UserListView.as_view()(factory.get("/", {"page": 99}))

    assert response.status_code == 404
    assert response.data["error"]["code"] == "NOT_FOUND"
