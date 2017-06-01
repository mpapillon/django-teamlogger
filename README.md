# TeamLogger, Django application

TeamLogger is a fully configured Django project for the [Nouvelles application](https://gitlab.com/mapapill/django-nouvelles-app).

## Run the app

First, clone the repo with dependencies :

```sh
git clone https://github.com/mpapillon/django-teamlogger.git
```

### Run locally

No configuration needed, just run the following commands :

```sh
# get requirements with pip
pip install -r app/requirements.txt

# run the server
./app/manage.py runserver
```

> :warning: TeamLogger doesn't work with python 2.

### Build and run with docker

> Docker container is based on [django-uwsgi-nginx](https://github.com/dockerfiles/django-uwsgi-nginx).

  * `docker build -t teamlogger .`
  * `docker run -d -p 80:80 teamlogger`
  * Go to 127.0.0.1 to see if works

---

## Settings

This section details wich environement variable you need to use to configure the application.

### Application settings

- `APP_SITE_NAME` : The name to show in headers.
   - Default: `TeamLogger`
   
- `APP_SITE_DOMAIN` : The domain of the site, like `http://www.example.com/`.
   - Default: `None`

- `APP_SITE_HEADLINES_DAYS` : The number of days to show in Headlines view.
   - Default: `7`

- `APP_EMAIL_HIGH_ARTICLES` : Allow the app to send mails when new article with high crtiticality is posted. If True, `APP_SITE_DOMAIN` is required.
   - Default: `False`

- `APP_DEBUG` : If True, runs the server in debug.
   - Default: `False`

- `APP_SECRET` : Specify the secret key to use with django.
   - Default: Auto generated

### Database settings

Database connection configuration is provided by the `DATABASE_URL` environment variable.
If no specifications, the default SQLITE databse is used.

Databases urls are like :

```
driver://user:passord@host/db_name
```

#### Supported Databases

You can use PostgreSQL, MySQL, Oracle, and SQLite.
   
### Email settings

See [Django Email Settings](https://docs.djangoproject.com/en/1.11/ref/settings/#email-host).
Most of default Django Email settings are mapped to an environment variable with the same name.

### LDAP Authentication Connection

LDAP Authentication is turned on when you set the `LDAP_AUTH_URL` env variable.

- `LDAP_AUTH_URL` : The URL of the LDAP server like `ldap://localhost:10389`.

- `LDAP_AUTH_USER_FIELDS` : JSON to map User model fields to ldap.
   - Default: `{ "username": "uid", "first_name": "cn", "last_name": "sn", "email": "mail" }`

- `LDAP_AUTH_USE_TLS` : Initiate TLS on connection.
   - Default: `False`

- `LDAP_AUTH_SEARCH_BASE` : The LDAP search base for looking up users.
   - Default: `ou=people,dc=example,dc=com`

- `LDAP_AUTH_CONNECTION_USERNAME` : The LDAP username of a user for querying the LDAP database for user details.
   - Default: `admin`

- `LDAP_AUTH_CONNECTION_PASSWORD` : The LDAP password of a user for querying the LDAP database for user details.
   - Default: `secret`

---

## Licence

Copyright (C) 2017  Maxence PAPILLON  
TeamLogger is under GPLv3. See the LICENCE file to know more.
