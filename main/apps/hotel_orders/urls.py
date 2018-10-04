# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.hotel_orders import views
router = routers.DefaultRouter()

router.register('hotel_order', views.HotelOrderViews, base_name='hotel_order')
router.register('pay_again', views.HotelOrderPayView, base_name='hotel_order_pay')
urlpatterns = router.urls
