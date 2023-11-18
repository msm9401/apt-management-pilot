#!/bin/sh

# This script checks if the container is started for the first time.
CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"

if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then

    touch /$CONTAINER_FIRST_STARTUP

    echo 'Running migrations...'
    python manage.py migrate --no-input

    #echo 'Saving apartment data...'
    #python manage.py get_houses

    echo 'Starting develop server...'
    python manage.py runserver 0.0.0.0:8000

else

    echo 'Starting develop server...'
    python manage.py runserver 0.0.0.0:8000
    
fi