# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04

LABEL maintainer "maxence.papillon@outlook.com"

ENV APP_PATH /home/docker/code/app/

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY docker/nginx-app.conf /etc/nginx/sites-available/default
COPY docker/supervisor-app.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY app/requirements.txt $APP_PATH
RUN pip3 install -r $APP_PATH/requirements.txt

# add (the rest of) our code
COPY app/ $APP_PATH
COPY docker/uwsgi_params /home/docker/code/
COPY docker/uwsgi.ini /home/docker/code/

# create required directories
RUN mkdir /home/docker/volatile
RUN mkdir -p /home/docker/persistent/databases

# set default admin
ENV APP_ADMIN_USERNAME admin
ENV APP_ADMIN_PASSW Pass

# copy starting script
COPY docker/docker-start-server.sh /home/docker
RUN chmod +rx /home/docker/docker-start-server.sh

EXPOSE 80
CMD ["/home/docker/docker-start-server.sh"]
