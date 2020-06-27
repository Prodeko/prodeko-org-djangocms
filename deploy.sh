#!/bin/bash

set -e

# Translations
python3 manage.py makemessages -l fi -i node_modules -i venv
python3 manage.py makemessages -d djangojs -l fi -i tiedotteet -i node_modules -i venv
python3 manage.py compilemessages -l fi

# SCSS
python3 manage.py compilescss

# Collect static to Azure storage account
python3 manage.py collectstatic --ignore=*.scss --noinput

# Delete compiled css files from local filesystem
python3 manage.py compilescss --delete-files