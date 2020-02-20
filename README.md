# lanve_django

MacOS + dockcer-compose(Python3.8 + Django3.1 + Mariadb + Nginx + uWsgi) + Bluma + Pycharm + AWS

## Description

This is my first web app powerd by Django.<br>
Its purpose is to help to exchange unfamiliar languages between each others.

## Setup

### Development environment
```
$ git clone git@github.com:ShuntaH/lanve_django.git
$ docker-compose up -d
$ charm .
$ docker exec -it lanve_web /bin/bash
$ cd django/project/
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic
```

* Development django server -> localhost:8001
* Nginx server -> localhost:8000

### Production environment
```
$ ssh -i aws ec2
$ docker-compose -f docker-compose-production.yml  up -d
$ docker exec -it lanve_web /bin/bash
$ cd django/project/
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py collectstatic
```
#### change configurations
* manage.py
* wsgi.py
```
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.production')
```

### Create .env file for SECRET INFORMATION <br>
* -/docker-compose.yml<br> 
* -/django/project/project/settings/*

### Pycharm Professinal
docker & debugger setting
