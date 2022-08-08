import os

from django.db import models
from cpf_field.models import CPFField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class RevendedorUser(AbstractUser):
    USERNAME_FIELD = 'cpf'
    nome_completo = models.CharField(max_length=200)
    cpf = CPFField('cpf', unique=True)
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return "{{'nome_completo': {0}, 'cpf': {1}}}".format(self.username, self.cpf)


class Compra(models.Model):
    REQUIRED_FIELDS = ['revendedor', 'codigo', 'valor', 'status']
    revendedor = models.ForeignKey(RevendedorUser, on_delete=models.CASCADE, to_field="cpf")
    codigo = models.CharField("código", max_length=100)
    valor = models.DecimalField("valor", max_digits=8, decimal_places=2)
    data = models.DateField("data")

    class Status(models.TextChoices):
        VALIDATION = 'V', _('Em validação')
        APPROVED = 'A', _('Aprovado')

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.VALIDATION,
    )

    porcentagem = \
        models.PositiveIntegerField("Porcentagem de cashback",
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    valor_cashback = models.DecimalField("valor", max_digits=8, decimal_places=2)

    @property
    def valor_display(self):
        return "R$%s" % self.valor

    def __str__(self):
        return self.codigo
