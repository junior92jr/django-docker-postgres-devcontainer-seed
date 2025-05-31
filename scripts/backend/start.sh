#!/bin/bash

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver "$APP_HOST":"$APP_PORT"