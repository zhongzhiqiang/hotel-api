# coding:utf-8
# Time    : 2018/9/1 下午1:55
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.banner import views

router = routers.DefaultRouter()

router.register('banner', views.BannerViews, base_name='banner')

urlpatterns = router.urls
