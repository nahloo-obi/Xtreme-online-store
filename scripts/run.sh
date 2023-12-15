#!/bin/sh

set -e

# Create necessary directories
# mkdir -p /app/staticfiles
# mkdir -p /static
# mkdir -p /media
# mkdir -p /vol


python manage.py wait_for_db
# python manage.py collectstatic --noinput
# python manage.py migrate

uwsgi --socket :9000 --workers 4 --master --enable-threads --module ecommerce.wsgi
