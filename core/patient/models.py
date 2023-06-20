from django.db import models
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator,MaxLengthValidator
from datetime import date

# Create your models here.
GENDER_OPTIONS = [
        ('MASCULINO', 'MASCULINO'),
        ('FEMENINO', 'FEMENINO'),
    ]

class Patient(models.Model):
    curp = models.CharField(
        verbose_name='CURP',
        max_length=18,
        blank=False,
        null=False,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{4}\d{6}[H,M][A-Z]{5}[A-Z0-9]\d$',
                message='El CURP no es válido'
            )
        ]
    )
    name = models.CharField(verbose_name='Nombre', max_length=150, blank=False,null=False)
    paternal_surname = models.CharField(verbose_name='Apellido Paterno', max_length=150, blank=False,null=False)
    maternal_surname = models.CharField(verbose_name='Apellido Materno', max_length=150, blank=False,null=False)
    gender = models.CharField(max_length=30, choices=GENDER_OPTIONS, verbose_name='Sexo')
    birthday_date = models.DateField(verbose_name='Fecha de Nacimiento',blank=True,null=True)
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
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['name']

    def toJSON(self):
        item = model_to_dict(self)
        item['birthday_date'] = self.birthday_date.strftime('%Y-%m-%d')
        return item