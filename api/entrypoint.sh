#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# --timeout 300: generating tailored application materials is a single long
# model call that runs well past gunicorn's 30s default, and the worker gets
# killed mid-request otherwise (shows up as a bare 500).
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 300
