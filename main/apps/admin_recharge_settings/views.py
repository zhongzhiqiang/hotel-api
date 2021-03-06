# coding:utf-8
# Time    : 2018/10/3 下午4:20
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import RechargeSettings, RechargeInfo
from main.common.permissions import PermsRequired
from main.apps.admin_recharge_settings import serializers, filters


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
    permission_classes = (PermsRequired('main.vip_info'), )

    def perform_create(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        else:
            serializer.save()


class RechargeInfoView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        返回所有用户充值记录
    retrieve:
        返回用户充值记录详情
    """
    queryset = RechargeInfo.objects.all()
    serializer_class = serializers.RechargeInfoSerializer
    filter_class = filters.RechargeInfoFilter
    permission_classes = (PermsRequired('main.vip_info'),)
