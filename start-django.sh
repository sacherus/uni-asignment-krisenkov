#!/bin/bash
set -xe

python manage.py collectstatic --noinput

exec gunicorn -c gunicorn.conf uni_assignment_metars.wsgi
