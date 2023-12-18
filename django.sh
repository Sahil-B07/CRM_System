#!/bin/sh

echo "Initialized migrations"
python manage.py makemigrations api
echo "=============================="

echo "Migrate instances"
python manage.py migrate

echo "Migrations ✅"
echo "=============================="

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
