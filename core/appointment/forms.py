from django.forms import *
from .models import *
from datetime import datetime
from core.doctor.models import Doctor
from core.appointment.models import Patient


class AppointmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
                
    class Meta:
        model = Appointment
        fields = '__all__'
    
    def save(self,commit = True):
        form = super()
        data = {}
        try:
            if(form.is_valid()):
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
                
        return data

class AppointmentByDoctorForm(Form):
    doctor = ModelChoiceField(queryset=Doctor.objects.all(),widget=Select(attrs={'class': 'form-control'}))

class AppointmentByPatientForm(Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].choices = self.get_custom_cli_choices()

    def get_custom_cli_choices(self):
        # Lógica para generar las opciones personalizadas
        choices = []
        choices.append(('','---------'))
        for obj in Patient.objects.all():
            label = f'{obj.curp} - {obj.get_full_name()}'
            choices.append((obj.id, label))
        return choices
    patient = ModelChoiceField(queryset=Patient.objects.all(),widget=Select(attrs={'class': 'form-control select2'}))
