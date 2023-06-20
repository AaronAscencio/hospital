from django.db import models
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator,MaxLengthValidator
from datetime import date
from core.doctor.models import Doctor
from core.patient.models import Patient
from core.nurse.models import Nurse
from core.office.models import Office

# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Paciente')
    office = models.ForeignKey(Office, on_delete=models.CASCADE, verbose_name='Consultorio')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Doctor')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE,verbose_name='Enfermera')
    date = models.DateField(verbose_name='Fecha de la Cita')
    time = models.TimeField(verbose_name='Hora de la Cita')

    def __str__(self):
        return f'Cita para {self.patient.get_full_name()} con el Dr. {self.doctor.get_full_name()}'
            
    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def toJSON(self):
        item = model_to_dict(self)
        item['patient'] = self.patient.get_full_name()
        item['doctor'] = self.doctor.get_full_name()
        item['nurse'] = self.nurse.get_full_name()
        item['office'] = self.office.toJSON()
        item['date'] = self.date.strftime('%Y-%m-%d')
        item['time'] = self.time.strftime("%I:%M %p")
        item['specialty'] = self.doctor.specialty.name
        return item
    
    def clean(self):
        super().clean()
        existing_appointment = Appointment.objects.filter(
            date=self.date,
            time=self.time,
            doctor=self.doctor
        ).exclude(pk=self.pk)
        if existing_appointment.exists():
            raise Exception('Ya se encuentra ocupado ese día con ese doctor.')
