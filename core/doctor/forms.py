from django.forms import *
from .models import *
from datetime import datetime


class DoctorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Doctor
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