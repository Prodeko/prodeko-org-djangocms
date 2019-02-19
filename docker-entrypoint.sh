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

# Collect static for the django installation.
python3 manage.py makemigrations

python3 manage.py collectstatic --noinput > /dev/null 2>&1

python3 manage.py migrate

# Load sample data for development
python3 manage.py loaddata --e contenttypes --app cms --app menus --verbosity 3 data.json

# Create a superuser for development
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='webbitiimi@prodeko.org').delete(); User.objects.create_superuser('webbitiimi@prodeko.org', 'kananugetti', has_accepted_policies=True)"

exec "$@"