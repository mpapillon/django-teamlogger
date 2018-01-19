# TeamLogger, Django application

Team Newspaper: This tool enhance the spread of valuable work or infos about a projet. 
TeamLogger focus on teamspirit and stress the importance of sharing between team members in order to keep a high 
level of transparency.

## Run the app

First, clone the repo with dependencies (recursive for jquery, milky-css and select2 submodules):

```sh
git clone --recursive https://github.com/mpapillon/django-teamlogger.git
```

### Run locally

No configuration needed, just run the following commands :

```sh
# get requirements with node
npm i
npm build

# get requirements with pip
pip install -r requirements_dev.txt

# set required env variables
export DJANGO_SETTINGS_MODULE=teamlogger.settings.development
export APP_SECRET=MySecretKey

# run the server
./manage.py runserver
```

> :warning: TeamLogger require Python >= 3.4

### Build and run with docker

TeamLogger can be launched with Docker, see the [wiki page](https://github.com/mpapillon/django-teamlogger/wiki/Docker-image).

## Settings

You can change the configuration by setting environment variables. All parameters are optional.

### Application settings

_More informations in the [wiki page](https://github.com/mpapillon/django-teamlogger/wiki/Application-settings)._

### Database settings

TeamLogger can use _SQLite_, _PostgreSQL_, _MySQL_ or _Oracle_ as database.

Set the `DATABASE_URL ` environement variable with an url like:

```
postgres://admin:secret@localhost:5432/teamlogger
```

_More informations in the [wiki page](https://github.com/mpapillon/django-teamlogger/wiki/Database-settings)._

### Email settings

To allow email sending, you can set the `EMAIL_URL` environement variable as below:

```
smtp://localhost:25
```

_More informations in the [wiki page](https://github.com/mpapillon/django-teamlogger/wiki/Email-settings)._

### LDAP Authentication Connection

LDAP authentication can be used by setting the `LDAP_URL`.
If you enable LDAP auth. you will always able to use database stored users.

Example of `LDAP_URL`:

```
ldap://uid=admin,ou=system:passw@ldap.example.com:389/ou=users,dc=example,dc=local
```

_More informations in the [wiki page](https://github.com/mpapillon/django-teamlogger/wiki/LDAP-settings)._

## Licence

Copyright (C) 2018  Maxence PAPILLON  
TeamLogger is under GPLv3. See the LICENCE file to know more.
