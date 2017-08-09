#!/bin/sh
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
        echo "${RED}==>${NC} ${2}";
        exit 1
    fi
}

if [ -z ${APP_SECRET+x} ]; then
    echo "${RED}==>${NC} The variable APP_SECRET is required.";
    echo "    Please, set a secret key and restart the container."
    exit 1
fi

# Database migration/creation
echo "${GREEN}==>${NC} Database migration"
python manage.py migrate
RETURN_CODE=$?

catch_error ${RETURN_CODE} "An error occurred during database migration.";

# Moving static files
echo "\n${GREEN}==>${NC} Collecting static files"
python manage.py collectstatic --clear --no-input -i *.less -i *.scss -i node_modules
RETURN_CODE=$?

catch_error ${RETURN_CODE} "An error occurred during the collect static command.";

echo "\n${GREEN}==>${NC} Stating the server"
gunicorn teamlogger.wsgi -b :8000 --log-file -

exit 0
