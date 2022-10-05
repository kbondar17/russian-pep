from django.forms import ModelForm,  TextInput, URLInput, ChoiceField, RadioSelect

from .models import AppointDoc, PersonsNAppointments


class DocForm(ModelForm):
    class Meta:
        model = AppointDoc
        fields = ('file_name', 'date', 'text_raw', 'url', 'author', 'region')

        widgets = {
            'url': URLInput(attrs={'size': '90'}),
            'author': TextInput(attrs={'size': '30'}),
        }


class PersonsNAppointmentsForm(ModelForm):
    appoint = 'appoint'
    resign = 'resign'
    actions = ((appoint, 'назначение'), (resign, 'отставка'))

    class Meta:
        model = PersonsNAppointments
        fields = ('person', 'action')

    action = ChoiceField(label='Действие', choices=actions, widget=RadioSelect)
