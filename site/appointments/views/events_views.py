from typing import *

from django.views.generic import ListView, DetailView
from appointments.models import PersonsNAppointments, Region
from django.db.models import F


class EventList(ListView):
    model = PersonsNAppointments
    template_name = 'appointments/persons/events_entrypoint.html'
    context_object_name = 'events'
    paginate_by: int = 7

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        params = self.request.GET.dict()
        action = params.get('action_option', '')

        context = super().get_context_data()
        context.update(params)  # чтобы оставались в поиске
        regions = [e[0]
                   for e in list(Region.objects.all().values_list('name'))]
        if not 'date' in self.kwargs.get('query', []):
            order = '-date'
        else:
            order = self.kwargs.get('query')
            order = 'date' if order == '-date' else '-date'
        context['date'] = order
        context['regions'] = regions
        context['action'] = action

        return context

    def get_queryset(self, **kwargs):
        params = self.request.GET.dict()
        order = '-date'
        if 'date' in self.kwargs.get('query', []):
            order = self.kwargs.get('query')

        action = params.get('action_option','')
        region = params.get('region_search', '')
        position_searh = params.get('position_search', '')
        name_search = params.get('name_search', '')
        
        persons_n_appointments = PersonsNAppointments.objects.\
            annotate(name=F('person__name'),
                     position=F('app_line__position'),
                     date=F('app_line__appoint_doc__date'),
                     region=F('app_line__appoint_doc__region__name'),
                     pers_id=F('person__id')
                     ).order_by(order)

        if action:
            persons_n_appointments = persons_n_appointments.filter(
                action=action)

        persons_n_appointments = persons_n_appointments.filter(
            name__istartswith=name_search, position__icontains=position_searh)

        if region:
            persons_n_appointments = persons_n_appointments.filter(
                region=region)
        return persons_n_appointments.values('id', 'name', 'position', 'date', 'action', 'pers_id', 'region')


class EventDetail(DetailView):
    model = PersonsNAppointments
    template_name = 'appointments/persons/event_detail.html'
    context_object_name = 'event'

    def get_queryset(self):
        pna = PersonsNAppointments.objects.\
            annotate(name=F('person__name'),
                     position=F('app_line__position'),
                     full_text=F('app_line__appoint_doc__text_raw'),
                     date=F('app_line__appoint_doc__date'),
                     pers_id=F('person__id')
                     ).order_by('-date')
        return pna.values('id', 'name', 'position', 'date', 'action', 'pers_id', 'full_text')
