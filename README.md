# TeamLogger, Django application

Team Newspaper: This tool enhance the spread of valuable work or infos about a projet. K'eude focus on teamspirit and stress the importance of sharing between team members in order to keep a high level of transparency.

## Run the app

First, clone the repo with dependencies :

```sh
git clone https://github.com/mpapillon/django-teamlogger.git
```

### Run locally

No configuration needed, just run the following commands :

```sh
# get requirements with pip
pip install -r requirements.txt

# run the server
./manage.py runserver
```

> :warning: TeamLogger require Python >= 3.4

### Build and run with docker

TeamLogger can be launched with Docker, see the [wiki page](https://github.com/mpapillon/django-teamlogger/wiki/Docker-image).

## Settings

You can change the configuration by setting environement variables. All parameters are optional.

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

LDAP authentification can be used by setting the `LDAP_URL`. If you enable LDAP auth. you will always able to use database stored users.

Example of `LDAP_URL`:

```
ldap://admin:passw@localhost:10389/ou=users,dc=srv-name,dc=local
```

_More informations in the [wiki page](https://github.com/mpapillon/django-teamlogger/wiki/LDAP-settings)._

## Licence

Copyright (C) 2017  Maxence PAPILLON  
TeamLogger is under GPLv3. See the LICENCE file to know more.
