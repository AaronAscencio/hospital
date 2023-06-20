from django.db import models

# Create your models here.
from django.db import models
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator,MaxLengthValidator
from datetime import date

GENDER_OPTIONS = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO'),
    ]

class Specialty(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150, blank=False,null=False)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Doctor(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length=150, blank=False,null=False)
    paternal_surname = models.CharField(verbose_name='Apellido Paterno', max_length=150, blank=False,null=False)
    maternal_surname = models.CharField(verbose_name='Apellido Materno', max_length=150, blank=False,null=False)
    gender = models.CharField(max_length=30, choices=GENDER_OPTIONS, verbose_name='Sexo')
    birthday_date = models.DateField(verbose_name='Fecha de Nacimiento',blank=True,null=True)
    specialty = models.ForeignKey(Specialty,on_delete=models.CASCADE,verbose_name='Especialidad')
    professional_license = models.CharField(verbose_name='Cedula Profesional',max_length=8,blank=False,null=False,unique=True,validators=[RegexValidator(r'^\d{5,8}$', 'La cedula profesional debe tener entre 5 y 8 digitos.')])
    street = models.CharField(verbose_name='Calle', max_length=100, blank=False,null=False)
    street_number = models.CharField(verbose_name='Numero', max_length=15, blank=False,null=False)
    neighborhood = models.CharField(verbose_name='Colonia', max_length=100, blank=False,null=False)
    zip = models.CharField(verbose_name='Codigo Postal', max_length=5, blank=False,null=False,validators=[RegexValidator(r'^\d{5}$', 'SOLO SE PERMITEN NUMEROS')])
    city = models.CharField(verbose_name='Municipio', max_length=100, blank=False,null=False)
    state = models.CharField(verbose_name='Estado', max_length=100, blank=False,null=False)
    telephone = models.CharField(verbose_name='Telefono', max_length=13, blank=False,null=False,unique=True)
    

    def get_full_name(self):
        return f'{self.name} {self.paternal_surname} {self.maternal_surname}'
    
    def __str__(self):
        return f'{self.get_full_name()}'
        
    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'
        ordering = ['name']

    def toJSON(self):
        item = model_to_dict(self)
        item['specialty'] = self.specialty.toJSON()
        return item