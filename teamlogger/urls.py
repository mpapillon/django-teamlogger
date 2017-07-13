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
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect(reverse('index'))),

    # ex: /
    url('^', include('django.contrib.auth.urls')),

    # ex: /nouvelles/
    url(r'^nouvelles/', include('nouvelles.urls')),

    # ex: /admin
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
