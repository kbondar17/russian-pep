import json
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

from appointments.models import AppointDoc, AppointLine, PersonsNAppointments, Region, Person

def upload_to_db(file):
    try:
        with open(file, encoding='utf-8') as f:
            data = json.load(f)

    except json.JSONDecodeError: 
        print('нет новых назначений!')
        return


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

