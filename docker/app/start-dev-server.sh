#!/bin/sh
echo "Rodando migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000