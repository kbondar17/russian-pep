import json
from pathlib import Path
from django.db.models import Count, F, Value

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from appointments.models import AppointDoc, AppointLine, PersonsNAppointments, Region, Person

def truncate():
    AppointDoc.objects.all().delete()
    AppointLine.objects.all().delete()
    PersonsNAppointments.objects.all().delete()
    Region.objects.all().delete()
    Person.objects.all().delete()

def upload_to_db(file):
    """загружает 570 + тестовых документов о назначениях в правительстве (напр. Белоусов, Абрамченко, Козлов)"""

    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    not_processed_persons = []
    docs_id = data.keys()
    for doc_id in docs_id:
        try:
            doc_data = data[doc_id]
            date = '-'.join(list(reversed(doc_data['date'].split('.'))))
            # region = Region.objects.filter(short_name=doc_data['region']).first()
            region, _ = Region.objects.get_or_create(name=doc_data.get('region','РФ'))
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
                    person, _ = Person.objects.get_or_create(name=pers) 
                    
                    # if not persons:
                    #     not_processed_persons.append(pers)

                    # for person_object in persons:
                    pna, _ = PersonsNAppointments.objects.get_or_create(app_line=app_line_object, person=person, action='appoint')
                    print('Загрузили ', pna, _)


                appointees = line['resignees']
                for pers in appointees:
                    pers = pers['lemm_name'] 
                    person, _ = Person.objects.get_or_create(name=pers) 
                    
                    
                    pna, _ = PersonsNAppointments.objects.get_or_create(app_line=app_line_object, person=person, action='resign')
                    print('Загрузили ', pna, _)
        except Exception as ex:
            print('ОШИБКА -- ',ex, doc_id)
    print('персоны не найдены: ', not_processed_persons)


def find_top_100():
    persons = Person.objects.annotate(appoints_count=Count('appointments')).values_list('name', 'appoints_count')
    sorted_pers = sorted(persons, key=lambda x : x[-1], reverse=True)
    print(sorted_pers)

def analyze():
    pna = PersonsNAppointments.objects.\
        annotate(name=F('person__name'), 
                position=F('app_line__position'),
                date=F('app_line__appoint_doc__date')
                )#.first()
    print(pna.values('name', 'position', 'date', 'action'))
    


def upload_test_files():
    # фед правительство и москва
    files = ['scripts/test_appoints.json','scripts/parsed_pravitelstvo_2012_2022.json','scripts/parsed_putin.json','scripts/results_2000_2012_pravit.json','scripts/results_2012_2022_moscow.json']
    for file in files:
        upload_to_db(file)


if __name__ == '__main__':
    upload_test_files()
# find_top_100() 
# run()
# truncate()
# analyze()