#!/bin/bash
# set -e
# cmd="$@"

python /app/manage.py migrate
python /app/manage.py runserver 0.0.0.0:8001
#uwsgi --ini /app/compose/production.ini