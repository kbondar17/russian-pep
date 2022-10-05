from django.contrib import admin
from django.db import connection
from django.urls import reverse
from django.utils.html import format_html_join, mark_safe

from .models import (AppointDoc, AppointLine, AppointPerson,
                     PersonsNAppointments, SelectPersonForAppointment)
from .forms import DocForm, PersonsNAppointmentsForm


class AppointLine_Inline(admin.StackedInline):
    model = AppointLine.persons.through
    template = r'admin/appointments/edit_inline/stacked.html'
    raw_id_fields = ["app_line"]
    readonly_fields = ['action', 'person', 'get_date']
    verbose_name = "Назначение"
    verbose_name_plural = "Назначения"
    extra = 0
    can_delete = True

    def get_date(self, obj):
        return obj.app_line.doc.date


class PersonInline(admin.StackedInline):
    form = PersonsNAppointmentsForm
    model = PersonsNAppointments
    extra = 0
    template = r'admin/appointments/edit_inline/stacked.html'
    verbose_name_plural = "События"
    raw_id_fields = ["person"]
    show_change_link = True
    can_delete = True


class AppointLine_Inline_for_Doc(admin.StackedInline):
    model = AppointLine
    template = r'admin/appointments/edit_inline/stacked.html'
    verbose_name_plural = 'Строки с назначениями'
    readonly_fields = ['position',
                       'linked_appoint_line', 'person_in_appoint_line']
    show_change_link = True
    extra = 0

    def person_in_appoint_line(self, obj):
        """все упомянутые в строке с назначением люди"""

        persons = obj.app_pers.values(
            'family_name', 'name', 'patronymic', 'id').order_by()
        for pers in persons:
            pers['link'] = reverse(
                'admin:declarations_person_change', args=[pers['id']])
            pers['full_name'] = ' '.join(
                (pers['family_name'], pers['name'], pers['patronymic']))

        persons_with_links = format_html_join(', ', '<a href="{}" target="_blank">{}</a>',
                                                    ((pers['link'], pers['full_name'])
                                                     for pers in persons))
        return persons_with_links

    person_in_appoint_line.short_description = 'Упомянутые персоны'

    def linked_appoint_line(self, obj):
        url = reverse('admin:appointments_appointline_change', args=[obj.id])
        return mark_safe(f'<a href="{url}" target="_blank">{obj}</a>')

    linked_appoint_line.short_description = 'Строка с назначением'


@admin.register(AppointDoc)
class DocAdmin(admin.ModelAdmin):
    title = 'это док о назначении'
    form = DocForm
    inlines = [AppointLine_Inline_for_Doc]


@admin.register(AppointLine)
class AppoLineAdmin(admin.ModelAdmin):
    model = AppointLine
    list_register = ('position', 'appoint_doc')
    list_filter = ['appoint_doc__date']
    inlines = [PersonInline]
    readonly_fields = ['get_doc_full_text', 'linked_appoint_doc']

    fieldsets = (
        (None, {
            'fields': ('linked_appoint_doc', 'raw_line', 'position',)
        }),
        ('Полный текст документа', {
            'classes': ('collapse',),
            'fields': ('get_doc_full_text',),
        }),
    )

    def linked_appoint_doc(self, doc):
        url = reverse('admin:appointments_appointdoc_change',
                      args=[doc.appoint_doc.id])
        return mark_safe(f'<a href="{url}" target="_blank">{doc.appoint_doc}</a>')

    linked_appoint_doc.short_description = 'Документ'

    def get_doc_full_text(self, obj):
        return obj.appoint_doc.text_raw

    get_doc_full_text.short_description = 'Полный текст документа'


@admin.register(AppointPerson)
class PersonAdmin(admin.ModelAdmin):
    model = AppointPerson

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(appointments__isnull=False).distinct()
        return qs

@admin.register(SelectPersonForAppointment)
class SelectPersonForAppointmentAdmin(admin.ModelAdmin):
    '''класс для персон с одинаковыми именами и назначениями'''

    search_fields = ['=id', 'family_name', 'name', 'patronymic', 'comment']
    list_display = ('name_with_link_to_person', 'appoints_n_ids')

    def name_with_link_to_person(self, obj):
        url = reverse('admin:declarations_person_change', args=[obj.id])
        return mark_safe(
            f'<a href="{url}">{obj.get_person_full_name()}</a> ( id: {obj.id} )'
        )

    name_with_link_to_person.short_description = "Имя"

    def appoints_n_ids(self, obj):
        appoints = obj.appointments.values_list('position')
        return format_html_join('\n', "<li>{}</li>",
                                ((e[0], ) for e in appoints))

    appoints_n_ids.short_description = 'Назначения'

    def get_queryset(self, request):
        duplicated_persons = self.get_persons_ids_with_same_appoints()
        people = super().get_queryset(request)
        people = people.prefetch_related('appointments')
        people = people.filter(id__in=duplicated_persons)
        people = people.distinct()
        return people

    def get_persons_ids_with_same_appoints(self):
        """находит айди одноименных персон, занимающих одинаковые позиции (дубликаты)"""

        same_names_n_appointments = '''select duplicated_app_lines from (select
				GROUP_CONCAT(concat(
						pers.id, '')
						separator ';')                      
                    AS duplicated_app_lines, pers.family_name, pers.name, pers.patronymic, count(pers.family_name) as count
                    from persons_n_appointments pna
                    left join declarations_person pers 
                    on pers.id=pna.person_id 
                    where pna.app_line_id is not null
                    group by pers.family_name, pers.name, pers.patronymic
                    order by family_name, name) as aa where count > 1
                    ;'''

        with connection.cursor() as cursor:
            cursor.execute(same_names_n_appointments)
            pers_with_same_appointments = cursor.fetchall()
            pers_with_same_appointments = [e for e in [
                set(e[0].split(';')) for e in pers_with_same_appointments] if len(e) > 1]
            pers_with_same_appointments = list(
                set().union(*pers_with_same_appointments))
            return pers_with_same_appointments

