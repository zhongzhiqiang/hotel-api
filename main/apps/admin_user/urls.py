# coding:utf-8
# Time    : 2018/9/10 下午8:37
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_user import views

router = routers.DefaultRouter()

router.register('staff_center', views.AdminUserViews, base_name='staff_center')

urlpatterns = router.urls
