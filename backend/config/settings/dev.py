"""Local development settings."""

from .base import *  # noqa: F403

DEBUG = True

# Browsable API in development only
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]
