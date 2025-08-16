#!/bin/sh
set -e

echo "Starting Celery Beat..."
celery -A backend beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler