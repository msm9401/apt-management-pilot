from .base import *

DEBUG = True

ALLOWED_HOSTS = []

DEV_APPS = [
    "debug_toolbar",
]

INSTALLED_APPS += DEV_APPS

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
