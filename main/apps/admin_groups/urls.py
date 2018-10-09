# coding:utf-8
# Time    : 2018/10/9 下午9:36
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework import routers

from main.apps.admin_groups import views

urlpatterns = [
    url(r'^perms/config/$', views.RolePermsConfig.as_view()),
]

router = routers.DefaultRouter()
router.register('role', views.RoleViews, base_name='role')

urlpatterns += router.urls
