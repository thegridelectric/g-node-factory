#!/bin/bash
rm db.sqlite3
cd src/gnf
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@gridworks-consulting.com', 'admin')" | python manage.py shell
cd ../..
