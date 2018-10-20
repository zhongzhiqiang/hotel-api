# coding:utf-8
# Time    : 2018/9/1 下午1:51
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_banner import views

router = routers.DefaultRouter()

router.register('banner', views.AdminBannerView, base_name='admin_banner')
router.register('notice', views.AdminNoticeView, base_name='admin_notice')

urlpatterns = router.urls
