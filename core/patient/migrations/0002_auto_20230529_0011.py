# Generated by Django 3.0.6 on 2023-05-29 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['name'], 'verbose_name': 'Paciente', 'verbose_name_plural': 'Pacientes'},
        ),
    ]