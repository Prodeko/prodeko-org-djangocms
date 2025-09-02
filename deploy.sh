#!/bin/bash

set -e

# Translations
uv run manage.py makemessages -l fi -i node_modules -i venv
uv run manage.py makemessages -d djangojs -l fi -i tiedotteet -i node_modules -i venv
uv run manage.py compilemessages -l fi

# SCSS
uv run manage.py compilescss

# Collect static to Azure storage account
uv run manage.py collectstatic --ignore=*.scss --noinput

# Delete compiled css files from local filesystem
uv run manage.py compilescss --delete-files
