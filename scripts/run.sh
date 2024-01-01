#!/bin/sh

set -e

# cd /var/lib/jenkins/workspace/testttt

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate
echo "Migrations has been done"
python manage.py create_super_user

uwsgi --socket :9000 --workers 4 --master --enable-threads --module ecommerce.wsgi
