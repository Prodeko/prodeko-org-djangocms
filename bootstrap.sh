# download the package lists from the repositories
apt-get update && apt-get install build-essential libssl-dev libffi-dev python3-dev gettext

# --- python ---
# set default python version to 3.5
ln -sf /usr/bin/python3.5 /usr/bin/python

# install pip
apt-get install -y python3-pip

# --- apache ---
# install packages
apt-get install -y apache2 libapache2-mod-wsgi

# remove default webroot
rm -rf /var/www

# symlink project as webroot
ln -fs /vagrant /var/www

# setup hosts file
VHOST=$(cat <<EOF
<VirtualHost *:80>
  DocumentRoot "/vagrant"
  ServerName localhost
  <Directory /vagrant>
    AllowOverride All
    Order Allow,Deny
    Allow From All
  </Directory>
</VirtualHost>
EOF
)
echo "${VHOST}" > /etc/apache2/sites-available/default

# enable apache rewrite module
a2enmod rewrite

# --- mysql ---

# install packages
echo mysql-server mysql-server/root_password select "vagrant" | debconf-set-selections
echo mysql-server mysql-server/root_password_again select "vagrant" | debconf-set-selections
apt-get install -y mysql-server-5.7 libmysqlclient-dev

# create database
mysql -uroot -pvagrant -e "DROP USER IF EXISTS 'prodekoorg'@'localhost';"
mysql -uroot -pvagrant -e "FLUSH PRIVILEGES;"
mysql -uroot -pvagrant -e "CREATE USER 'prodekoorg'@'localhost' IDENTIFIED BY 'prodekoorg';"
mysql -uroot -pvagrant -e "GRANT ALL PRIVILEGES on *.* TO 'prodekoorg'@'localhost';"
mysql -uroot -pvagrant -e "DROP DATABASE IF EXISTS prodekoorg;"
mysql -uroot -pvagrant -e "CREATE DATABASE prodekoorg;"
mysql -uroot -pvagrant -e "DROP DATABASE IF EXISTS auth_db;"
mysql -uroot -pvagrant -e "CREATE DATABASE auth_db;"

# --- Required python modules ---
pip3 install -r /vagrant/requirements.txt
pip3 install --upgrade google-auth-oauthlib

# tasks
cd /vagrant && python3 manage.py makemigrations --noinput
#cd /vagrant && python3 manage.py migrate auth_prodeko --database=auth_db
cd /vagrant && python3 manage.py migrate

# creating an admin user
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='webbitiimi@prodeko.org').delete(); User.objects.create_superuser('webbitiimi@prodeko.org', 'kananugetti')" | python manage.py shell

# run server and static file watcher in screen
su - ubuntu -c "cd /vagrant && screen -S server -d -m python3 manage.py runserver 0.0.0.0:8000"
su - ubuntu -c "cd /vagrant && screen -S watcher -d -m python3 manage.py collectstatic"
su - ubuntu -c "cd /vagrant && screen -S watcher -d -m python3 manage.py watchstatic"

# --- restart apache ---

service apache2 restart

# fixes pip 'locale.Error: unsupported locale setting' error and ascii decode errors
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8