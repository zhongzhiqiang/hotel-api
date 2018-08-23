# coding:utf-8
# Time    : 2018/8/23 下午9:35
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import routers

from main.apps.integral import views

router = routers.DefaultRouter()

router.register('integral', views.UserIntegralView, base_name='integral')

urlpatterns = router.urls
