#!/bin/bash

set -e

function wait_for_db () {
	# Check if database is up and accepting connections.
  echo "Checking database connection"
  until psql $DATABASE_URL -c "select 1" 2>/dev/null; do
		>&2 echo "Database is unavailable - sleeping"
		sleep 1
	done
	>&2 echo "Database is up - continuing"
}

wait_for_db

# Create and run migrations
echo "Creating migrations..."
uv run manage.py makemigrations
uv run manage.py migrate

# Create a superuser for development
echo "Creating superuser..."
uv run manage.py shell -c "from django.contrib.auth import get_user_model; \
	User = get_user_model(); User.objects.filter(email='webbitiimi@prodeko.org').exists() or \
	User.objects.create_superuser('webbitiimi@prodeko.org', 'kananugetti', has_accepted_policies=True)"

# Load sample data for development
uv run manage.py loaddata --app cms --app menus --verbosity 3 data.json

# Translations
uv run manage.py makemessages -l fi -i "node_modules/*" -i "venv/*"
uv run manage.py makemessages -d djangojs -l fi -i tiedotteet -i "node_modules/*" -i "venv/*"
uv run manage.py compilemessages -l fi

exec "$@"
