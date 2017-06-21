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
NC='\033[0m'

# Database migration/creation
echo "${GREEN}==>${NC} Database migration"

python manage.py migrate

# Moving static files
echo "\n${GREEN}==>${NC} Collecting static files"
python manage.py collectstatic --clear --no-input

echo "\n${GREEN}==>${NC} Stating the server"
gunicorn teamlogger.wsgi -b :8000 --log-file -
