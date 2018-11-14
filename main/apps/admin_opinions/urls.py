# coding:utf-8
# Time    : 2018/11/14 下午10:08
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import routers

from main.apps.admin_opinions import views
router = routers.DefaultRouter()

router.register('opinions', views.AdminOpinionsViews, base_name='admin_opinion')

urlpatterns = router.urls
