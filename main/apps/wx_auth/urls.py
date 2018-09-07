# coding:utf-8
# Time    : 2018/9/6 下午9:33
# Author  : Zhongzq
# Site    : 
# File    : urls.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.wx_auth import views

router = routers.DefaultRouter()

router.register('auth', views.WeiXinAuth, base_name='auth')
router.register('user_center', views.UserCenterView, base_name='user_center')
urlpatterns = router.urls
