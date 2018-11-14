# coding:utf-8
# Time    : 2018/11/14 下午10:12
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import routers

from main.apps.opinions import views


router = routers.DefaultRouter()

router.register('opinion', views.OpinionsViews, base_name='opinion')

urlpatterns = router.urls
