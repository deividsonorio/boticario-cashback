import os
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revendedor', '0003_compra'),
    ]

    def generate_superuser(apps, schema_editor):
        from revendedor.models import RevendedorUser

        django_superuser_username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        django_superuser_email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        django_superuser_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        superuser = RevendedorUser.objects.create_superuser(
            cpf=django_superuser_username,
            username=django_superuser_username,
            email=django_superuser_email,
            password=django_superuser_password)

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
