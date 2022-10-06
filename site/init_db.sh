#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --no-input --username=kirill  --email=joe@example.com
python -m scripts.load

uwsgi --ini app/uwsgi.ini > logs/uwsgi_logs &
celery -A app worker --concurrency=1 -s /home/celery/var/run/celerybeat-schedule --loglevel=info -B &> logs/celery_beats.logs &