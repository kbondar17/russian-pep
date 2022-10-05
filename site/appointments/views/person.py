from typing import *

from appointments.models import Person
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import DetailView


class PersonDetail(DetailView):
    template_name = 'appointments/persons/person_detail.html'
    model = Person
    context_object_name = 'person'
    success_url = reverse_lazy('decrees:show_all_docs')

    def get_context_data(self, *args, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        pers = context['person']
        pers: Person
        positions = pers.appointments.annotate(date=F('appoint_doc__date'), full_text=F(
            'appoint_doc__text_raw')).order_by('-date').all()
        context['positions'] = positions
        return context
