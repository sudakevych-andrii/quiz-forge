"""Unified API error format: {"error": {"code": ..., "message": ...}}."""

from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


class ApiError(exceptions.APIException):
    """Base class for domain errors with an explicit machine-readable code.

    Subclass it per error, e.g.:

        class TestNotFound(ApiError):
            status_code = 404
            default_code = "TEST_NOT_FOUND"
            default_detail = "Test not found"
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "BAD_REQUEST"
    default_detail = "Bad request"


def exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    # Same conversions DRF does internally, so we can read code/detail below
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, DjangoPermissionDenied):
        exc = exceptions.PermissionDenied()

    response = drf_exception_handler(exc, context)
    if response is None or not isinstance(exc, exceptions.APIException):
        # Unhandled exception: Django returns 500 (traceback page in DEBUG)
        return response

    error: dict[str, Any]
    if isinstance(exc, exceptions.ValidationError):
        error = {
            "code": "VALIDATION_ERROR",
            "message": "Invalid input",
            "details": exc.detail,
        }
    else:
        error = {
            "code": str(exc.get_codes()).upper(),
            "message": str(exc.detail),
        }

    response.data = {"error": error}
    return response
