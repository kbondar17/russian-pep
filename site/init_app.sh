#!/bin/bash
uwsgi --ini app/uwsgi.ini > logs/uwsgi_logs &
#python -m celery -A app worker --concurrency=1 -s /home/celery/var/run/celerybeat-schedule --loglevel=info -B &> logs/celery_beats.logs &
