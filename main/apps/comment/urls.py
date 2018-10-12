# coding:utf-8
# Time    : 2018/10/12 下午9:58
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.comment import views

router = routers.DefaultRouter()

router.register('comment', views.CommentViews, base_name='comment')

urlpatterns = router.urls
