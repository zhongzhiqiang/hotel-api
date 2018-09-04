# coding:utf-8
# Time    : 2018/9/4 下午10:30
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_consumer import views

router = routers.DefaultRouter()

router.register('consumer', views.AdminConsumerView, base_name='consumer')

urlpatterns = router.urls
