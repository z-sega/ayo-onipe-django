"""Development settings."""

from .base import *  # noqa
from .base import BASE_DIR
import os  # noqa

print("Using development settings...")


ALLOWED_HOSTS = ["*"]

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email settings
# --- terminal
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# --- mail-service
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = os.getenv("EMAIL_HOST")
# EMAIL_PORT = os.getenv("EMAIL_PORT")
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# Debug
DEBUG = True

# Static
STATIC_ROOT = BASE_DIR / "staticfiles"
