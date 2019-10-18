#!/bin/bash

set -e

function wait_for_mysql () {
	# Check if MySQL is up and accepting connections.
	HOSTNAME=$(python <<EOF
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
o = urlparse('$DATABASE_URL')
print(o.hostname)
EOF
)
	until mysqladmin ping --host "$HOSTNAME" --silent; do
		>&2 echo "MySQL is unavailable - sleeping"
		sleep 1
	done
	>&2 echo "MySQL is up - continuing"
}

wait_for_mysql

# Create test database
# mysql -h db -P 3306 -u root -p$*secret -e "CREATE DATABASE test_prodekoorg;"
# mysql -h db -P 3306 -u root -p$*secret -e "GRANT ALL PRIVILEGES ON test_prodekoorg.* TO prodekoorg@localhost IDENTIFIED BY 'secret';"

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput > /dev/null 2>&1

# Create and run migrations
echo "Creating migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Create a superuser for development
echo "Creating superuser..."
python manage.py shell -c "from django.contrib.auth import get_user_model; \
	User = get_user_model(); User.objects.filter(email='webbitiimi@prodeko.org').exists() or \
	User.objects.create_superuser('webbitiimi@prodeko.org', 'kananugetti', has_accepted_policies=True)"

# Load sample data for development
python3 manage.py loaddata --app cms --app menus --verbosity 3 data.json

# Translations
python3 manage.py makemessages -l fi
python3 manage.py makemessages -d djangojs -l fi -i tiedotteet -i node_modules
python3 manage.py compilemessages -l fi

exec "$@"