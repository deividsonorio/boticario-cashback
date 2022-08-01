from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RevendedorUser


class CustomUserAdmin(UserAdmin):
    fieldset = (
        *UserAdmin.fieldsets,
        (
            'Informacoes do Revendedor',
            {
                'fields': (
                    'nome_completo',
                    'cpf'
                )
            }
        )
    )


admin.site.register(RevendedorUser)
admin.site.site_header = "Administração | Teste Boticário"
admin.site.site_title = "Administração | Teste Boticário"
admin.site.index_title = "Bem vindo ao sistema"