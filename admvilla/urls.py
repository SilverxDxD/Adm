"""admvilla URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),

    # DataTabke
    # url(r'^table/', include('table.urls')),
    url(r'^table/', include('apps.inicio.table.urls')),

    # Select2
    url(r'^select2/', include('django_select2.urls')),

    url(r'^inicio/', include('apps.inicio.urls', namespace='inicio')),
    url(r'^servicio/', include('apps.servicios.urls', namespace='servicio')),
    url(r'^reusables/', include('apps.reusables.urls', namespace='reusables')),
]
