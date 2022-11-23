#!/bin/bash
cd src/gnf
rm django_related/db.sqlite3
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@gridworks-consulting.com', 'admin')" | python manage.py shell
cd ../..
