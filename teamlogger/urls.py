"""TeamLogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import re
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.conf.urls import include, url
from django.contrib import admin
from nouvelles.admin import admin_page
from teamlogger.settings import APP_CONTEXT

context_path = re.sub(r'^/', '', APP_CONTEXT)

urlpatterns = [
    url(r'^'+context_path+r'$', lambda r: HttpResponseRedirect(reverse('index'))),
    
    # ex: /
    url('^'+context_path, include('django.contrib.auth.urls')),

    # ex: /nouvelles/
    url(r'^'+context_path+r'nouvelles/', include('nouvelles.urls')),

    # ex: /admin
    url(r'^'+context_path+r'admin/', admin_page.urls),
]
