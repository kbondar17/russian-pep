from datetime import datetime
from celery import shared_task, task
from pathlib import Path
import json

from appointments.models import AppointDoc, AppointLine, Region, Person, PersonsNAppointments

from pravo_api import PravoApi

regions = []

@task
def test_apps():
    from datetime import datetime
    print(f'время: {datetime.now()}', )

def load_data_to_db(filepath):

    with open(Path(filepath).parent.absolute() / 'files/test_appoints.json', encoding='utf-8') as f:
        data = json.load(f)

    not_processed_persons = []
    docs_id = data.keys()
    for doc_id in docs_id:
        doc_data = data[doc_id]
        date = '-'.join(list(reversed(doc_data['date'].split('.'))))
        region = Region.objects.filter(short_name=doc_data['region']).first()
        if not region:
            print(f'{doc_data["region"]} нет такого региона')

        doc, _ = AppointDoc.objects.get_or_create(id=doc_data['doc_id'], region=region,
                                                  file_name=doc_data['file_name'], file_path=doc_data['file_path'],
                                                  date=date, text_raw=doc_data['text_raw'], url=doc_data['url'],
                                                  author=doc_data['author'])

        app_lines = doc_data['appointment_lines']
        for line in app_lines:
            position = line['position']
            raw_line = line['raw_line']
            app_line_object, _ = AppointLine.objects.get_or_create(appoint_doc=doc,
                                                                   raw_line=raw_line, position=position)

            appointees = line['appointees']
            for pers in appointees:
                pers = pers['lemm_name']
                persons = Person.find_by_fullname(pers)

                if not persons:
                    not_processed_persons.append(pers)

                for person_object in persons:
                    pna, _ = PersonsNAppointments.objects.get_or_create(
                        app_line=app_line_object, person=person_object, action='appoint')
                    print('Загрузили ', pna, _)

            appointees = line['resignees']
            for pers in appointees:
                pers = pers['lemm_name']
                persons = Person.find_by_fullname(pers)

                if not persons:
                    not_processed_persons.append(pers)

                for person_object in persons:
                    pna, _ = PersonsNAppointments.objects.get_or_create(
                        app_line=app_line_object, person=person_object, action='resign')
                    print('Загрузили ', pna, _)

    print('персоны не найдены: ', not_processed_persons)

log_file = 'appoints.log'
temp_data = 'appoints_data'

def get_regional_apps():
    for reg in regions:
        output_file = f'{reg}.json'
        with open(output_file, 'w') as _:
            ...
        today = datetime.today().strftime('%d-%m-%Y')
        api = PravoApi(
                REGION=reg, 
                DATA_FOLDER=temp_data,
                FROM_DATE=today, TO_DATE=today,
                log_file=log_file 
                )
        api.get_appoints(output_file)

def get_federal_appoints():
    fed_bodies = []
    region = 'РФ'
    for body in fed_bodies:
        output_file = f'{body}.json'
        with open(output_file, 'w') as _:
            ...
        today = datetime.today().strftime('%d-%m-%Y')
        
        api = PravoApi(
                REGION=region,
                FEDERAL_GOVERNMENT_BODY=body,
                DATA_FOLDER=temp_data,
                FROM_DATE=today, TO_DATE=today,
                log_file=log_file 
                )
        api.get_appoints(output_file)


