# coding:utf-8
# Time    : 2018/9/8 下午9:03
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.market_order import views


router = routers.DefaultRouter()

router.register('market_order', views.MarketOrderViews, base_name='market_order')

urlpatterns = router.urls
