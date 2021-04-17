#!/usr/bin/env bash
set -xe

./manage.py makemigrations --check
TESTS_ENABLED=1 ./manage.py test --no-input

celery worker -A uni_assignment_metars& sleep 5 && celery -A uni_assignment_metars status
