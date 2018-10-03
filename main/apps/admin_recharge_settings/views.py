# coding:utf-8
# Time    : 2018/10/3 下午4:20
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import RechargeSettings
from main.apps.admin_recharge_settings import serializers


class RechargeSettingsView(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    create:
        创建充值配置
    update:
        更新充值配置
    retrieve:
        充值配置详情
    list:
        所有充值配置
    """
    queryset = RechargeSettings.objects.all()
    serializer_class = serializers.RechargeSettingsSerializer

    def perform_create(self, serializer):
        serializer.save()
