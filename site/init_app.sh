#!/bin/bash
uwsgi --ini app/uwsgi.ini &
celery -A app.my_celery worker -B