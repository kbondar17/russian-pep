#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --no-input --username=kirill  --email=aa@bb.com
python -m scripts.load
