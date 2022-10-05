#!/bin/bash
python manage.py migrate
python manage.py collectstatic -y
python manage.py createsuperuser --no-input --username=kirill  --email=joe@example.com
python -m scripts.load
uwsgi --ini app/uwsgi.ini --attach-daemon2 'cmd=celery -A app worker --concurrency=1 -s /home/celery/var/run/celerybeat-schedule --loglevel=info -B &> logs/celery_beats.logs'

