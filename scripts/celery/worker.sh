#!/bin/sh
set -e

echo "Starting Celery Worker..."
celery -A backend worker --loglevel=info