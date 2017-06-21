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

LABEL maintainer "maxence.papillon@outlook.com"

WORKDIR /usr/src/app

# get requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy all files into container
COPY . .

# set static and media directories to use
ENV APP_STATIC_ROOT=/srv/app/static
ENV APP_MEDIA_ROOT=/srv/app/media

# create static and media directories
RUN mkdir -p $APP_STATIC_ROOT
RUN mkdir -p $APP_MEDIA_ROOT

# make starting script runable
RUN chmod +rx docker-start-server.sh

EXPOSE 8000
VOLUME ["/var/log/", "/usr/src/app/", "$APP_STATIC_ROOT", "$APP_MEDIA_ROOT"]

CMD ["/usr/src/app/docker-start-server.sh"]
