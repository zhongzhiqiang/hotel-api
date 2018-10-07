# coding:utf-8
# Time    : 2018/10/4 下午6:42
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.recharge import views


router = routers.DefaultRouter()

router.register('recharge_settings', views.RechargeSettingsViews, base_name='recharge_settings')
router.register('recharge', views.RechargeViews, base_name='recharge')
router.register('recharge_again', views.RechargeAgainPayView, base_name='recharge_again')

urlpatterns = router.urls
