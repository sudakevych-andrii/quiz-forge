from unittest.mock import ANY

import pytest
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from common.exceptions import ApiError

factory = APIRequestFactory()


class QuizNotFound(ApiError):
    status_code = 404
    default_code = "TEST_NOT_FOUND"
    default_detail = "Test not found"


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RaisingView(APIView):
    """GET raises `exc`; POST validates an email."""

    permission_classes = [AllowAny]
    exc: Exception = ApiError()

    def get(self, request: Request) -> Response:
        raise self.exc

    def post(self, request: Request) -> Response:
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


@pytest.mark.parametrize(
    ("exc", "status_code", "code"),
    [
        (QuizNotFound(), 404, "TEST_NOT_FOUND"),
        (ApiError(), 400, "BAD_REQUEST"),
        (Http404(), 404, "NOT_FOUND"),
        (DjangoPermissionDenied(), 403, "PERMISSION_DENIED"),
    ],
)
def test_errors_use_unified_format(exc: Exception, status_code: int, code: str) -> None:
    response = RaisingView.as_view(exc=exc)(factory.get("/"))

    assert response.status_code == status_code
    assert response.data == {"error": {"code": code, "message": ANY}}


def test_domain_error_message() -> None:
    response = RaisingView.as_view(exc=QuizNotFound())(factory.get("/"))

    assert response.data["error"]["message"] == "Test not found"


def test_validation_error_includes_field_details() -> None:
    request = factory.post("/", {"email": "not-an-email"}, format="json")
    response = RaisingView.as_view()(request)

    assert response.status_code == 400
    assert response.data == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid input",
            "details": {"email": ["Enter a valid email address."]},
        }
    }


def test_authentication_is_required_by_default() -> None:
    class PrivateView(APIView):
        def get(self, request: Request) -> Response:
            return Response()

    response = PrivateView.as_view()(factory.get("/"))

    assert response.data["error"]["code"] == "NOT_AUTHENTICATED"
    assert PrivateView.permission_classes == [IsAuthenticated]


def test_unhandled_exception_is_not_swallowed() -> None:
    with pytest.raises(RuntimeError):
        RaisingView.as_view(exc=RuntimeError("boom"))(factory.get("/"))
