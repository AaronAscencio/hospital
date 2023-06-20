from django.db import models
from django.forms.models import model_to_dict
from django.conf import settings
from datetime import datetime
from core.patient.models import Patient
from core.product.models import Product
from core.doctor.models import Doctor

# Create your models here.
class Sale(models.Model):
    cli = models.ForeignKey(Patient, on_delete=models.CASCADE)
    diagnostic = models.CharField(max_length=50, blank=False, null=False)
    treatment = models.CharField(max_length=350, blank=False, null=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def get_image(self):
        return '{}{}'.format(settings.STATIC_URL, 'img/logo.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.get_full_name()
        item['cli_id'] = self.cli.id
        item['doctor'] = self.doctor.get_full_name()
        item['specialty'] = self.doctor.specialty.name
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        return f'{self.pk} - {self.cli.get_full_name()} - ${self.total}'

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

    def toJSON(self):
        item = model_to_dict(self,exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price,'.2f')
        item['subtotal'] = format(self.subtotal,'.2f')
        return item