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

from main.apps.wx_pay import views

docs_url = get_swagger_view(u'宾馆API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', docs_url),
    url(r'^auth/', ObtainJSONWebToken.as_view()),
    url(r'^user/', include('main.apps.market.urls')),
    url(r'^user/', include('main.apps.hotels.urls')),
    url(r'^user/', include('main.apps.integral.urls')),
    url(r'^user/', include('main.apps.distribution.urls')),
    url(r'^user/', include('main.apps.banner.urls')),
    url(r'^user/', include('main.apps.wx_auth.urls')),
    url(r'^user/', include('main.apps.orders.urls')),
    url(r'^user/', include('main.apps.recharge.urls')),
    url(r'^user/', include('main.apps.comment.urls')),
    url(r'^user/', include('main.apps.cart.urls')),
    url(r'^admin/', include('main.apps.admin_market.urls')),
    url(r'^admin/', include('main.apps.admin_hotels.urls')),
    url(r'^admin/', include('main.apps.admin_integral.urls')),
    url(r'^admin/', include("main.apps.admin_images.urls")),
    url(r'^admin/', include('main.apps.admin_order.urls')),
    url(r'^admin/', include('main.apps.admin_distribution.urls')),
    url(r'^admin/', include('main.apps.admin_banner.urls')),
    url(r'^admin/', include('main.apps.admin_consumer.urls')),
    url(r'^admin/', include('main.apps.admin_user.urls')),
    url(r'^admin/', include('main.apps.admin_tags.urls')),
    url(r'^admin/', include('main.apps.admin_marketorder.urls')),
    url(r'^admin/', include('main.apps.admin_recharge_settings.urls')),
    url(r'^admin/', include('main.apps.admin_comment.urls')),
    url(r'^admin/', include('main.apps.admin_groups.urls')),
    url(r'^admin/', include('main.apps.admin_vip.urls')),
    url(r'^admin/', include("main.apps.admin_refunded.urls")),
    url(r'^notify/$', views.ReceiveWXNotifyView.as_view()),
    url(r'^user/status_search/$', views.OrderStatusSearchView.as_view())
]
