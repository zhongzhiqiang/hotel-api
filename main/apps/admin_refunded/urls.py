# coding:utf-8
# Time    : 2018/10/20 下午10:34
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_refunded import views


router = routers.DefaultRouter()

router.register('market_refunded', views.MarketRefundedViews, base_name='market_refunded')
router.register('hotel_refunded', views.HotelRefundedViews, base_name='hotel_refunded')

urlpatterns = router.urls
