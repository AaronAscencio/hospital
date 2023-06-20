from django.forms import *
from .models import *
from datetime import datetime
from core.doctor.models import Doctor
from core.appointment.models import Patient


class ClinicalHistoryByPatientForm(Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].choices = self.get_custom_cli_choices()
        self.fields['patient'].widget.attrs['class'] = 'form-control select2'

    def get_custom_cli_choices(self):
        # Lógica para generar las opciones personalizadas
        choices = []
        choices.append(('','---------'))
        for obj in Patient.objects.all():
            label = f'{obj.curp} - {obj.get_full_name()}'
            choices.append((obj.id, label))
        return choices
    patient = ModelChoiceField(queryset=Patient.objects.all(),widget=Select(attrs={'class': 'form-control select2'}))