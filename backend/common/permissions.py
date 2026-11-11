from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminRole(BasePermission):
    """Allow only authenticated users with role ADMIN (the app's admins).

    Not to be confused with DRF's IsAdminUser, which checks is_staff
    (access to Django Admin).
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        return bool(user.is_authenticated and getattr(user, "is_admin", False))
