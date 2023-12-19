"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

django_settings_env = os.environ.get("DJANGO_SETTINGS_ENV", "config.settings.develop")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_env)

application = get_asgi_application()
