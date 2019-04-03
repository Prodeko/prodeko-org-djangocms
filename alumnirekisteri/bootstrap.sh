
# download the package lists from the repositories
apt-get update


# --- python ---

# set default python version to 3.4
ln -sf /usr/bin/python3.4 /usr/bin/python

# install pip
apt-get install -y python3-pip
# upgrades pip to fix this issue: https://stackoverflow.com/questions/34371266/django-1-9-installation-syntaxerror-invalid-syntax
pip3 install --upgrade pip

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
apt-get install -y mysql-server-5.5 libmysqlclient-dev

# create database
mysql -uroot -pvagrant -e "CREATE USER 'alumnirekisteri'@'localhost' IDENTIFIED BY 'alumnirekisteri';"
mysql -uroot -pvagrant -e "GRANT ALL PRIVILEGES on *.* TO 'alumnirekisteri'@'localhost';"
mysql -uroot -pvagrant -e "CREATE DATABASE alumnirekisteri;"


# --- Required python modules ---
# full dependency list specified in requirements.text. django-pipeline caused problems.
pip3 install --no-deps -r /vagrant/requirements.txt

# tasks
# cd /vagrant && python manage.py syncdb --noinput
cd /vagrant && python manage.py makemigrations rekisteri
cd /vagrant && python manage.py migrate

# Create superuser
cd /vagrant && echo "from rekisteri.initialise import *; create_admin_profile();" | python manage.py shell

# Run server and static file watcher in screen
su - vagrant -c "cd /vagrant && screen -S server -d -m python manage.py runserver 0.0.0.0:8000"
su - vagrant -c "cd /vagrant && screen -S watcher -d -m python manage.py watchstatic"

# --- restart apache ---

service apache2 restart
