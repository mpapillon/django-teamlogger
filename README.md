# TeamLogger, Django application

TeamLogger is a fully configured Django project for the [Nouvelles application](https://gitlab.com/mapapill/django-nouvelles-app).

## Build and run with docker

> Docker container is based on [django-uwsgi-nginx](https://github.com/dockerfiles/django-uwsgi-nginx).

  * `docker build -t teamlogger .`
  * `docker run -d -p 80:80 teamlogger`
  * Go to 127.0.0.1 to see if works
