#!/bin/sh

python manage.py collectstatic --noinput
gunicorn chatbot.wsgi -b 0.0.0.0:8000