# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.orders import views
router = routers.DefaultRouter()

router.register('order', views.OrderViews, base_name='order')
router.register('pay_again', views.OrderPayView, base_name='order_pay')
urlpatterns = router.urls
