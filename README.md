# lanve_django

MacOS + dockcer-compose(Python3.8 + Django3.1 + Mariadb + Nginx + uWsgi) + Bluma + Pycharm + AWS

## Description

This is my first web app powerd by Django.<br>
Its purpose is to help to exchange unfamiliar languages between each others.

## Setup

Development environment
```
$ git clone git@github.com:ShuntaH/lanve_django.git
$ docker-compose up -d
$ charm .
```

### Development django server -> localhost:8001
### Nginx server -> localhost:8000


* Pycharm Professinal
docker & debugger setting

### Create .env file for SECRET INFORMATION<br>
-/docker-compose.yml database <br> 
-/django/project/project/settings/base.py secretkey&database
