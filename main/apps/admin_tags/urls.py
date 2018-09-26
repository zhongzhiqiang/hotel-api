# coding:utf-8
# Time    : 2018/9/26 下午9:06
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_tags import views


router = routers.DefaultRouter()

router.register('tags', views.TagViews, base_name='tags')

urlpatterns = router.urls
