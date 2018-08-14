# coding:utf-8
"""hotel_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view
from rest_framework_jwt.views import ObtainJSONWebToken

docs_url = get_swagger_view(u'宾馆API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', docs_url),
    url(r'^auth/', ObtainJSONWebToken.as_view()),
    url(r'^user/', include('main.apps.market.urls')),
    url(r'^user/', include('main.apps.hotels.urls'))

]
