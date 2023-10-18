#!/bin/bash

set -e

#echo "Change DJANGO_SETTINGS_MODULE from develop to service..."
#export DJANGO_SETTINGS_MODULE=config.settings.service

echo 'Starting gunicorn...'
gunicorn config.wsgi:application --bind 0.0.0.0:8000 -c ./gunicorn/config.py