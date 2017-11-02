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
"""TeamLogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
import re
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from nouvelles.admin import admin_page

from django.contrib.auth import views as auth
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

context_path = re.sub(r'^/', '',  getattr(settings, 'APP_CONTEXT'))

urlpatterns = [url(r'^'+context_path, include([
    url('^', include('django.contrib.auth.urls')),
    url('^', include('nouvelles.urls')),
    url(r'^login/$', auth.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin_page.urls)
]))]

if settings.DEBUG:
    import debug_toolbar

    # Turn on Django Debug Toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # Adding urls for MEDIA files in debug
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()


