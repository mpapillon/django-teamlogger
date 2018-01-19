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

_term() {
  echo "\n${GREEN}==>${NC} Stopping server..."
  kill -TERM ${pid}
}

# Basic configuration
CONFIG_FLAG=/opt/initialized

if [ ! -f ${CONFIG_FLAG} ] ; then
	echo -e "\n${GREEN}==>${NC} First time configuration..."

	nginx_conf_file=/etc/nginx/sites-available/default

	# Apply context settings on nginx.conf
	if [ ! -z "$APP_CONTEXT" ] ; then
		sed -i "s#&context#/${APP_CONTEXT}#g" $nginx_conf_file
		ret_code=$?
	else
		sed -i "s#&context##g" $nginx_conf_file
		ret_code=$?
	fi

	sed -i "s#&static_root#${APP_STATIC_ROOT}#g" $nginx_conf_file
	ret_code=$[ret_code+$?]

	sed -i "s#&media_root#${APP_MEDIA_ROOT}#g" $nginx_conf_file
	ret_code=$[ret_code+$?]

	if [ ${ret_code} -eq 0 ] ; then
		touch ${CONFIG_FLAG}
 	else
		echo -e "\n${RED}==>${NC} First time configuration got errors: ${ret_code}"
		exit 1
 	fi
fi

# Database migration/creation
echo -e "${GREEN}==>${NC} Database migration"
python manage.py migrate
RETURN_CODE=$?

catch_error ${RETURN_CODE} "An error occurred during database migration.";

# Moving static files
echo -e "\n${GREEN}==>${NC} Collecting static files..."
python manage.py collectstatic --verbosity=0 --clear --no-input -i *.less -i *.scss -i node_modules
RETURN_CODE=$?

catch_error ${RETURN_CODE} "An error occurred during the collect static command.";

echo -e "\n${GREEN}==>${NC} Stating the server"

trap _term SIGTERM
supervisord
pid=$!

wait "${pid}"

exit 0
