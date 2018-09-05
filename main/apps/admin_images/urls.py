# coding:utf-8
# Time    : 2018/8/28 下午3:30
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_images import views

router = routers.DefaultRouter()
router.register('image', views.ImageViews, base_name='image')

urlpatterns = router.urls
