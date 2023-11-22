#!/bin/sh

# dockerize -wait tcp://postgres:5432 -timeout 100s
# dockerize -wait tcp://redis:6379 -timeout 100s

# This script checks if the container is started for the first time.
CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"

if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then

    touch /$CONTAINER_FIRST_STARTUP

    echo 'Running migrations...'
    python manage.py migrate --no-input

    #echo 'Saving apartment data...'
    #python manage.py get_houses

    echo 'Saving apartment data...'
    python manage.py loaddata apartment.json

    echo 'Starting develop server...'
    python manage.py runserver 0.0.0.0:8000

else

    echo 'Starting develop server...'
    python manage.py runserver 0.0.0.0:8000
    
fi