from django.forms import *
from .models import *
from datetime import datetime
from core.patient.models import Patient


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].choices = self.get_custom_cli_choices()
        self.fields['doctor'].choices = self.get_custom_doctor_choices()

    def get_custom_cli_choices(self):
        # Lógica para generar las opciones personalizadas
        choices = []
        choices.append(('','---------'))
        for obj in Patient.objects.all():
            label = f'{obj.curp} - {obj.get_full_name()}'
            choices.append((obj.id, label))
        return choices
    
    def get_custom_doctor_choices(self):
        # Lógica para generar las opciones personalizadas
        choices = []
        choices.append(('','---------'))
        for obj in Doctor.objects.all():
            label = f'{obj.professional_license} - {obj.get_full_name()}'
            choices.append((obj.id, label))
        return choices
        
    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width 50%',
                }
            ),
            'doctor': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width 50%',
                }
            ),
           'date_joined': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete':'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'diagnostic': TextInput(attrs={
                'class': 'form-control',
            }),
            'treatment': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }
        exclude = ['user_updated', 'user_creation']
    
class SaleByDoctorForm(Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].choices = self.get_custom_doctor_choices()

    def get_custom_doctor_choices(self):
        # Lógica para generar las opciones personalizadas
        choices = []
        choices.append(('','---------'))
        for obj in Doctor.objects.all():
            label = f'{obj.professional_license} - {obj.get_full_name()}'
            choices.append((obj.id, label))
        return choices
    doctor = ModelChoiceField(queryset=Doctor.objects.all(),widget=Select(attrs={'class': 'form-control'}))