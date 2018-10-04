# coding:utf-8
# Time    : 2018/10/4 下午6:44
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm

from rest_framework import routers

from main.apps.admin_recharge_settings import views


router = routers.DefaultRouter()

router.register('recharge_settings', views.RechargeSettingsView, base_name='admin_recharge_settings')

urlpatterns = router.urls
