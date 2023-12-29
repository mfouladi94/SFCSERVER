#!/bin/bash

# Make migrations
python manage.py makemigrations

# Migrate
python manage.py migrate

# collect static
python manage.py collectstatic --no-input


# Run Django runserver
gunicorn --bind 0.0.0.0:8000 djangoApiBoilerPlate.wsgi