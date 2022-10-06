import os

from celery import Celery
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

django.setup()

redis_url_1 = f'redis://{os.environ["redis_host"]}'
redis_url_2 = f'redis://{os.environ["redis_host"]}:{os.environ["redis_port"]}/2'
 
app = Celery('celery_app', 
                broker=redis_url_1,
                backend=redis_url_2,
                ) 

app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from app.celery_tasks.tasks import get_new_appointments
    sender.add_periodic_task(60*60*24, get_new_appointments)
                                    
if __name__ == '__main__':
    app.start()
