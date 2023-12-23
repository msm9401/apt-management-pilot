import os
from pathlib import Path
from datetime import timedelta


SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-&!0&y+zz$6w+i7m9+=0*h12af*gs^dkcr0xnjdomfio1lisd)c"
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = int(os.environ.get("DEBUG", 1))

if os.environ.get("DJANGO_ALLOWED_HOSTS"):
    ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
else:
    ALLOWED_HOSTS = []

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "common.apps.CommonConfig",
    "notices.apps.NoticesConfig",
    "contacts.apps.ContactsConfig",
    "complaints.apps.ComplaintsConfig",
    "schedule.apps.ScheduleConfig",
    "polls.apps.PollsConfig",
    "houses.apps.HousesConfig",
    "feeds.apps.FeedsConfig",
    "comments.apps.CommentsConfig",
    "medias.apps.MediasConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "knox",
    "corsheaders",
    "storages",
    "django_prometheus",
    "guest_user",
]

INSTALLED_APPS = SYSTEM_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework.authentication.SessionAuthentication",
        "knox.auth.TokenAuthentication",
    ],
    "EXCEPTION_HANDLER": "config.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # it should be the last entry to prevent unauthorized access
    "guest_user.backends.GuestBackend",
]

# default "guest_user.functions.generate_uuid_username"
GUEST_USER_NAME_GENERATOR = "guest_user.functions.generate_numbered_username"
GUEST_USER_NAME_PREFIX = "일단구경만"  # default "Guest"
GUEST_USER_NAME_SUFFIX_DIGITS = 6  # default 4
GUEST_USER_MAX_AGE = 21600  # 6시간

REST_KNOX = {
    "TOKEN_TTL": timedelta(weeks=4),  # default: 10
    "TOKEN_LIMIT_PER_USER": 4,  # default: None
}

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://:apt_management_password@redis:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         },
#     }
# }

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3001", "http://localhost:3001"]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3001"]
