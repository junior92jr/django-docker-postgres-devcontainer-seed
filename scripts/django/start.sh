#!/bin/bash
set -e

echo "Running Django migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000