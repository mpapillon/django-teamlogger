#!/bin/bash
# K'eude
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

# Database migration/creation
python3 $APP_PATH/manage.py migrate

# Moving static files
python3 $APP_PATH/manage.py collectstatic --clear --no-input

# Create an administrator if not yet created
python3 $APP_PATH/manage.py shell -c "from django.contrib.auth.models import User; 

if not User.objects.filter(is_superuser=True).count():
    User.objects.create_superuser('$APP_ADMIN_USERNAME', '$APP_ADMIN_EMAIL', '$APP_ADMIN_PASSW')
"

supervisord -n