import socket
import colorlog
import logging
from json_log_formatter import JSONFormatter

from .base import *


DEBUG = True

ALLOWED_HOSTS = ["*"]

DEV_APPS = [
    "debug_toolbar",
]

DEV_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += DEV_APPS

MIDDLEWARE += DEV_MIDDLEWARE

INTERNAL_IPS = [
    "127.0.0.1",
]

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1"]

# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",
#    }
# }


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

TARGET_ATTR = [
    "levelname",
    "name",
    "module",
    "funcName",
    "lineno",
    "filename",
    "pathname",
    "created",
]


class CustomisedJSONFormatter(JSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        # https://github.com/marselester/json-log-formatter/blob/master/json_log_formatter/__init__.py
        extra.update(
            {
                attr_name: record.__dict__[attr_name]
                for attr_name in record.__dict__
                if attr_name in TARGET_ATTR
            }
        )

        extra["message"] = message or record.message
        request = extra.pop("request", None)

        if request is not None:
            try:
                extra["x_forward_for"] = request.META.get("X-FORWARD-FOR")
            except:
                extra["x_forward_for"] = request
        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)
        else:
            extra["exc_info"] = None
        return extra


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": colorlog.ColoredFormatter,
            "format": "%(log_color)s [%(asctime)s] [%(levelname)-8s] [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": CustomisedJSONFormatter,
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "formatter": "json",
            "encoding": "utf-8",
            "filename": "./logs/django.log",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": [],
        },
    },
    "loggers": {
        logger_name: {
            "level": "INFO",
            "propagate": True,
        }
        for logger_name in (
            "django",
            "django.request",
            # "django.db.backends",
            # "django.template",
        )
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}
