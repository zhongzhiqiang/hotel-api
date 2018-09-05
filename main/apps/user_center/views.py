# coding:utf-8
# Time    : 2018/9/5 下午9:58
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import Consumer

from main.apps.user_center import serializers


class UserCenterView(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
        update:
            更新用户信息
        list:
            返回当前登录用户信息
        retrieve:
            返回当前用户详细信息
    """
    serializer_class = serializers.ConsumerSerializer
    queryset = Consumer.objects.all()
