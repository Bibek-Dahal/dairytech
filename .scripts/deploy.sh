#!/bin/bash
set -e

echo "Deployment started ..."

# Pull the latest version of the app
git pull origin main
echo "New changes copied to server !"

# Activate Virtual Env
source source /home/merodairy/virtualenv/dairyapp/dairytech/3.9/bin/activate
echo "Virtual env 'mb' Activated !"

echo "Installing Dependencies..."
pip install -r requirements.txt --no-input

echo "Serving Static Files..."
python manage.py collectstatic --noinput

echo "Running Database migration"
python manage.py makemigrations
python manage.py migrate

# Deactivate Virtual Env
deactivate
echo "Virtual env 'mb' Deactivated !"

# Reloading Application So New Changes could reflect on website
# pushd miniblog
# touch wsgi.py
# popd

echo "Deployment Finished!"