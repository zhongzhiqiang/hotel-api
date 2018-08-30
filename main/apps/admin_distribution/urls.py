# coding:utf-8
# Time    : 2018/8/30 下午8:49
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_distribution import views

router = routers.DefaultRouter()

router.register('apply', views.AdminDistributionApplyView, base_name='apply')
router.register('pick', views.BonusPickViews, base_name='pick_view')

urlpatterns = router.urls
