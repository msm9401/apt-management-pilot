import os
from pathlib import Path


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
]

INSTALLED_APPS = SYSTEM_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
        "knox.auth.TokenAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": "config.exceptions.custom_exception_handler",
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:apt_management_password@redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

AWS_ACCESS_KEY_ID = "AKIAR53U574K3ZDTLRNE"
AWS_SECRET_ACCESS_KEY = "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"
AWS_REGION = "ap-northeast-2"

# S3 Storages
AWS_STORAGE_BUCKET_NAME = "apt-management-bucket"
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
AWS_DEFAULT_ACL = "public-read"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATIC_URL = "https://%s/static/" % AWS_S3_CUSTOM_DOMAIN

LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000", "http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000"]
