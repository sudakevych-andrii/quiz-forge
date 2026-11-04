"""Production settings."""

from .base import *  # noqa: F403

DEBUG = False

# Behind Nginx: trust X-Forwarded-Proto to detect HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
