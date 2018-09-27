# coding:utf-8
# Time    : 2018/9/26 下午9:50
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_marketorder import views

router = routers.DefaultRouter()

router.register('market_order', views.MarketOrderView, base_name='market_order')

urlpatterns = router.urls
