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


# ===== python manage.py test 실행 시 로깅 설정 무시 =====
# https://docs.python.org/ko/3.8/library/sys.html#sys.argv
# python manage.py test 명령 수행하면
# sys.argv[1] = test, len(sys.argv) = 2
# import sys

# if len(sys.argv) > 1 and sys.argv[1] == "test":
#     logging.disable(logging.CRITICAL)
# ======================================================

# Docker 개발 환경 실행 시 DEV_LOGGING에서 LOGGING으로 이름 변경.
# Docker 개발 환경 실행 시 logs폴더 존재 여부 확인(없으면 오류). 아래 "filename" 참고.
DEV_LOGGING = {
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
