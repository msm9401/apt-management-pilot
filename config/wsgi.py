"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

django_settings_env = os.environ.get("DJANGO_SETTINGS_ENV", "config.settings.develop")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings_env)

application = get_wsgi_application()
