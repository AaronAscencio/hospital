from django.db import models
from django.forms.models import model_to_dict

# Create your models here.

class Office(models.Model):
    number = models.PositiveIntegerField(verbose_name='Numero del Consultorio',blank=False,null=False,unique=True)

    class Meta:
        verbose_name = 'Consultorio'
        verbose_name_plural = 'Consultorios'

    def toJSON(self):
        return model_to_dict(self)
    
    def __str__(self):
        return f'Consultorio No. {self.number}'
    
    