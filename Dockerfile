# TeamLogger
# Copyright (C) 2017  Maxence PAPILLON
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

FROM python:3.6

LABEL maintainer=maxence.papillon@outlook.com

# set static and media directories to use
ENV APP_PATH=/usr/src/app
ENV LOGS_PATH=/var/log
ENV APP_STATIC_ROOT=/srv/app/static
ENV APP_MEDIA_ROOT=/srv/app/media

# set application in production mode
ENV DJANGO_SETTINGS_MODULE=teamlogger.settings.production

# Install required packages and remove the apt packages cache when done
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	nginx \
	supervisor
RUN rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_PATH}

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY docker/conf/nginx.conf /etc/nginx/sites-available/default
COPY docker/conf/supervisord.conf /etc/supervisor/conf.d/

EXPOSE 8000
VOLUME ["${LOGS_PATH}", "${APP_PATH}", "${APP_STATIC_ROOT}", "${APP_MEDIA_ROOT}"]

STOPSIGNAL SIGTERM

# get requirements
COPY src/requirements_prod.txt src/requirements.txt ${APP_PATH}/
RUN pip install --no-cache-dir -r requirements_prod.txt

# copy app files into container
COPY src/ ${APP_PATH}/

# create static and media directories
RUN mkdir -p ${APP_STATIC_ROOT} ${APP_MEDIA_ROOT}

# make starting script runable
COPY docker/docker-start-server.sh ${APP_PATH}/
RUN chmod +x docker-start-server.sh

CMD ["./docker-start-server.sh"]
