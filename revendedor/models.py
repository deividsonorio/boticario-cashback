from django.db import models
from cpf_field.models import CPFField
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class RevendedorUser(AbstractUser):
    USERNAME_FIELD = 'cpf'
    nome_completo = models.CharField(max_length=200)
    cpf = CPFField('cpf', unique=True)
    REQUIRED_FIELDS = ['username']


class Compra(models.Model):
    revendedor = models.ForeignKey(RevendedorUser, on_delete=models.CASCADE, to_field="cpf")
    codigo = models.CharField("código", max_length=100)
    valor = models.DecimalField("valor", max_digits=8, decimal_places=2)
    data = models.DateField("data", auto_now_add=True)

    VALIDATION = 'v'
    APPROVED = 'A'
    STATUS_OPCOES = [
        (VALIDATION, 'Em validação'),
        (APPROVED, 'Aprovado'),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS_OPCOES,
        default=VALIDATION,
    )

    porcentagem = \
        models.PositiveIntegerField("Porcentagem de cashback",
                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    valor_cashback = models.DecimalField("valor", max_digits=8, decimal_places=2)

    @property
    def valor_display(self):
        return "R$%s" % self.valor