from django.db import models
from cpf_field.models import CPFField
from django.contrib.auth.models import AbstractUser


class RevendedorUser(AbstractUser):
    USERNAME_FIELD = 'cpf'
    nome_completo = models.CharField(max_length=200)
    cpf = CPFField('cpf', unique=True)
    REQUIRED_FIELDS = ['username']
