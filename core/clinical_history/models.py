from django.db import models
from core.doctor.models import Doctor
from core.patient.models import Patient
from core.office.models import Office
from core.sale.models import Sale
from django.forms.models import model_to_dict

# Create your models here.
class ClinicalHistory(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    name_doctor = models.CharField(max_length=50, blank=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True)
    name_patient = models.CharField(max_length=50, blank=True, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True)
    diagnostic = models.CharField(max_length=50, blank=False, null=False)


    class Meta:
        verbose_name = 'Historial Clinico'
        verbose_name_plural = 'Historiales Clinicos'
    
    def __str__(self):
        return f'{self.pk}'
    
    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.date.strftime('%Y-%m-%d')
        item['doctor'] = self.doctor.get_full_name()
        item['patient'] = self.patient.get_full_name()
        item['sale'] = self.sale.toJSON()
        return item
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo registro
            if self.doctor:
                self.name_doctor = self.doctor.get_full_name()
            if self.patient:
                self.name_patient = self.patient.get_full_name()
            if self.sale:
                self.diagnostic = self.sale.diagnostic

        super().save(*args, **kwargs)

    


