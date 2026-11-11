from datetime import timedelta

import pytest
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from apps.accounts.models import User

factory = APIRequestFactory()


class WhoAmIView(APIView):
    """Protected by the default permission (IsAuthenticated)."""

    def get(self, request: Request) -> Response:
        return Response({"user": str(request.user)})


def get(token: str | None = None) -> Response:
    if token:
        request = factory.get("/", HTTP_AUTHORIZATION=f"Bearer {token}")
    else:
        request = factory.get("/")
    response: Response = WhoAmIView.as_view()(request)
    return response


def test_valid_access_token_authenticates(user: User) -> None:
    response = get(str(AccessToken.for_user(user)))

    assert response.status_code == 200
    assert response.data == {"user": "user@example.com"}


def test_missing_token_returns_401() -> None:
    response = get()

    assert response.status_code == 401
    assert response["WWW-Authenticate"].startswith("Bearer")
    assert response.data["error"]["code"] == "NOT_AUTHENTICATED"


@pytest.mark.django_db
def test_invalid_token_returns_401() -> None:
    response = get("not-a-jwt")

    assert response.status_code == 401
    assert response.data == {
        "error": {
            "code": "TOKEN_NOT_VALID",
            "message": "Given token not valid for any token type",
        }
    }


def test_expired_token_returns_401(user: User) -> None:
    token = AccessToken.for_user(user)
    token.set_exp(lifetime=-timedelta(seconds=1))

    response = get(str(token))

    assert response.status_code == 401
    assert response.data["error"]["code"] == "TOKEN_NOT_VALID"


def test_inactive_user_is_rejected(user: User) -> None:
    token = str(AccessToken.for_user(user))
    user.is_active = False
    user.save()

    response = get(token)

    assert response.status_code == 401
