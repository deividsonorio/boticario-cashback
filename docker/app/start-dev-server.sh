#!/bin/sh
echo "Rodando migrations..."
python manage.py makemigrations
python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('08360313938', 'teste@boticario.com', 'teste123', cpf='08360313938', first_name='Teste', last_name='Boticario')"
echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000