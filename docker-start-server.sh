#!/bin/bash
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

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

catch_error() {
    if [ $1 -gt 0 ]; then
        echo -e "${RED}==>${NC} ${2}";
        exit 1
    fi
}

if [ -z ${APP_SECRET+x} ]; then
    echo -e "${RED}==>${NC} The variable APP_SECRET is required.";
    echo -e "    Please, set a secret key and restart the container."
    exit 1
fi

## Basic configuration
CONFIG_FLAG=/opt/initialized

if [ ! -f ${CONFIG_FLAG} ] ; then
	echo -e "\n${GREEN}==>${NC} Starting basic configuration..."

	echo -e "\n    ${GREEN}==>${NC} Configure Apache HTTPD"
	RAND_KEY="$(rand-keygen -s 16)-$(rand-keygen -s 16)-$(rand-keygen -s 16)-$(rand-keygen -s 16)"

	SITE_NAME="${APP_SITE_NAME:-Teamlogger}"
	SITE_CONTEXT="${APP_CONTEXT:-/}"
	SECRET_KEY="${APP_SECRET:-${RAND_KEY}}"
	SITE_NAME="${APP_SITE_NAME:-Teamlogger}"
	SITE_CONTEXT="${APP_CONTEXT:-/}"
	SECRET_KEY="${APP_SECRET:-${RAND_KEY}}"

	echo "
export LANG='en_US.UTF-8'
export LC_ALL='en_US.UTF-8'

export APP_SITE_NAME=\"${SITE_NAME}\"
export APP_SECRET=\"${SECRET_KEY}\"
export APP_CONTEXT=\"${SITE_CONTEXT}\"
" >> /etc/apache2/envvars
	ret_code=$?

	sed -i 's/80/8000/g;s/443/8001/g' /etc/apache2/ports.conf
	ret_code=$[ret_code+$?]
	cp ${APP_PATH}/httpd/conf/000-default.conf /etc/apache2/sites-available/000-default.conf
	ret_code=$[ret_code+$?]

	# Configure apache rights
	echo -e "\n    ${GREEN}==>${NC} Configure Apache folders rights"
	usermod -G root www-data
	ret_code=$[ret_code+$?]
	chmod -R 775 ${APP_STATIC_ROOT} ${APP_MEDIA_ROOT}
	ret_code=$[ret_code+$?]
	chown -R www-data:root ${APP_STATIC_ROOT} ${APP_MEDIA_ROOT}
	ret_code=$[ret_code+$?]

	# Timezone Settings
	TIME_ZONE=${TZ:-Etc/UTC}
	echo -e "\n    ${GREEN}==>${NC} Configure Time Zone to ${TIME_ZONE}"
	echo "${TIME_ZONE}" > /etc/timezone
	ret_code=$[ret_code+$?]
	ln -fs /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
	ret_code=$[ret_code+$?]
	dpkg-reconfigure --frontend noninteractive tzdata
	ret_code=$[ret_code+$?]

	if [ ${ret_code} -eq 0 ] ;then
		touch ${CONFIG_FLAG}
		echo -e "\n${GREEN}==>${NC} Basic configuration done"
	else
		echo -e "\n${RED}==>${NC} Basic configuration got errors: ${ret_code}"
	fi
fi

# Database migration/creation
echo -e "${GREEN}==>${NC} Database migration"
python manage.py migrate
RETURN_CODE=$?

catch_error ${RETURN_CODE} "An error occurred during database migration.";

# Moving static files
echo -e "\n${GREEN}==>${NC} Collecting static files"
python manage.py collectstatic --clear --no-input -i *.less -i *.scss -i node_modules
RETURN_CODE=$?

catch_error ${RETURN_CODE} "An error occurred during the collect static command.";

echo -e "\n${GREEN}==>${NC} Stating the server"
# gunicorn teamlogger.wsgi -b :8000 --log-file -

apache2ctl restart || apache2ctl stop && apache2ctl start

tail -f /var/log/apache2/access.log -f /var/log/apache2/error.log &
pid="$!"

trap "echo -e \"\n${GREEN}==>${NC} Stopping server\"; kill -SIGTERM ${pid}" SIGINT SIGTERM

while kill -0 ${pid} > /dev/null 2>&1; do
    wait
done

apache2ctl stop

exit 0
