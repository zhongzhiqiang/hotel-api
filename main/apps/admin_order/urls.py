# coding:utf-8
# Time    : 2018/8/28 下午9:49
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_order import views

router = routers.DefaultRouter()

router.register('hotel_order', views.AdminHotelOrderInfoView, base_name='hotel_order')

urlpatterns = router.urls