#!/bin/sh

set -e

mkdir var
cd var
mkdir lib
cd lib
mkdir jenkins
cd jenkins
mkdir workspace
cd workspace
mkdir testttt
cd testttt
# cd /var/lib/jenkins/workspace/testttt

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate
echo "Migrations has been done"

uwsgi --socket :9000 --workers 4 --master --enable-threads --module ecommerce.wsgi
