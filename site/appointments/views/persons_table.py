from typing import *

from appointments.models import Person
from django.db.models import Count
from django.views.generic import ListView

class PersonsList(ListView):
    model = Person
    template_name = 'appointments/persons/person_entrypoint.html'
    context_object_name = 'persons'
    paginate_by: int = 10

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        params = self.request.GET.dict()
        context = super().get_context_data(**kwargs)
        context.update(params)
        return context

    def get_queryset(self):
        params = self.request.GET.dict()
        name_search = params.get('name_search', '')
        position_searh = params.get('position_search', '')
        sorted_pers = Person.objects.annotate(appoints_count=Count('appointments', distinct=True)).order_by('-appoints_count')
        filtered = sorted_pers.filter(name__istartswith=name_search, appointments__position__icontains=position_searh)
        return filtered

    
