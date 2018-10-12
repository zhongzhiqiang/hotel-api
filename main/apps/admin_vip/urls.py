# coding:utf-8
# Time    : 2018/10/12 下午10:39
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_vip import views

router = routers.DefaultRouter()

router.register('vip_member', views.VipMemberViews, base_name='vip_member')
router.register('vip_settings', views.VipSettingsViews, base_name='vip_settings')

urlpatterns = router.urls
