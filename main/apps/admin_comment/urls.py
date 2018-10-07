# coding:utf-8
# Time    : 2018/10/7 下午10:44
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_comment import views

router = routers.DefaultRouter()
router.register('comment_replay', views.HotelOrderCommentViews, base_name='comment_replay')

urlpatterns = router.urls
