# Installation and Development

## Introduction

Anyone who might find this application useful is free to fork the project and 
modify or further develop it. That said, this project has been designed and 
developed with Prodeko's needs and environment in mind, so it is unlikely that
it would work for others without any tuning. However, I have written a short
description how to deploy the application and get started in developing it in
a local environment.

## Structure
The application can be seen consisting of three main parts: 1) Client application, 2) API, and 3) 
Admin site. 

### Client
The client application is JavaScript app developed with React. The production build of
the client application is just a static HTML page injected with a javascript bundle.
The javascript code handles user interactions and renders content to the page based 
on data fetched from the API service.

### API
The API which provides data to the application is produced by a Python application 
running on a linux server. The server application is developed using Django framework. 

### Admin site
The admin site differs from the public site (the client app) in that it is not a static
javascript app, but it is rather based on server side rendering. It uses more traditional 
Model-View-Controller (MVC) pattern in which the pages are created by the Django application
using views (Python functions) and templates (HTML with Django template tags).

## Local environment setup

### Start the server
In order to run the application locally, we will need a linux machine. The easiest way is
to install Oracle's VirtualBox and Vagrant by HashiCorp. Then we can just go the the root
directory (where is Vagrantfile) and run

``` 
vagrant up 
```  

In the first time, Vagrant installs an ubuntu instance on a virtual machine based
on specifications in the Vagrantfile. It also installs python dependencies in 
requirements.txt.

When the vagrant box is running, the application can be opened on a browser at
[http://127.0.0.1:9000](http://127.0.0.1:9000). The url routes have been defined
in Tiedotteet/urls.py. The admin site pages are under /cp path.


### Create a user

In order to log in to the app, create the first user on the command line/terminal. 
When vagrant is running, in the project root folder, run
``` 
vagrant ssh 
cd /vagrant
python manage.py createsuperuser
```  

Then follow the instructions (provide username and password, email can be empty).

- Vagrant ssh takes ssh connection to the virtual machine. 

- /vagrant is the shared
folder between vagrant and the host machine, containing the source files. 

- python manage.py createsuperuser is Django stuff and it allows to create an admin user
to the database (which is sqlite by default).


### Build the client application

In order to see the public client application at "/" running, the app needs to be built.
First, install the required node modules specified in client/package.json. 
``` 
cd client
npm install
``` 
when the installation has been finished, build the javascript bundle:
``` 
npm run start
```

When the build completes, go to [http://127.0.0.1:9000](http://127.0.0.1:9000) root
and the application should now be visible.

## Deployment
TODO