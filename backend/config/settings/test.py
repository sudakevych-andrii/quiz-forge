"""Settings for the pytest run."""

from .base import *  # noqa: F403

DEBUG = False

# Argon2 is deliberately slow; tests don't need strong hashes
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
