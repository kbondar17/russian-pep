from datetime import datetime
from pathlib import Path

from app.my_celery import app
from pravo_api import PravoApi
from app.celery_tasks.db_uploader import upload_to_db


data_folder = Path('app/celery_tasks/data').absolute()

@app.task()
def get_new_appointments():
    """получает новые назначения и загружает их в БД"""
    today = datetime.strftime(datetime.today(),'%d.%m.%Y')
    api = PravoApi(
                    FEDERAL_GOVERNMENT_BODY='Правительство', 
                    DATA_FOLDER=data_folder,    
                    FROM_DATE='12.07.2022', TO_DATE=today,
                    log_file='my_custom.log' 
                    )
    output_filename = 'app/celery_tasks/results.json'
    api.get_appoints(output_filename)
    upload_to_db(output_filename)




