# coding:utf-8
# Time    : 2018/8/29 下午10:29
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.distribution import views

router = routers.DefaultRouter()

router.register('distribution', views.DistributionApplyView, base_name='distribution')
router.register('pick_bonus', views.DistributionBonusPickViews, base_name='pick_bonus')
router.register('bonus_detail', views.DistributionDetailView, base_name='bonus_detail')

urlpatterns = router.urls
