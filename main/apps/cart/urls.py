# coding:utf-8
# Time    : 2018/10/15 下午11:08
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.cart import views

router = routers.DefaultRouter()

router.register('cart', views.CartViews, base_name='cart')

urlpatterns = router.urls
