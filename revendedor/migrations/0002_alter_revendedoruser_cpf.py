# Generated by Django 4.0.6 on 2022-07-29 19:38

import cpf_field.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revendedor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revendedoruser',
            name='cpf',
            field=cpf_field.models.CPFField(max_length=14, unique=True, verbose_name='cpf'),
        ),
    ]
