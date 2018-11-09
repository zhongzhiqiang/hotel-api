# coding:utf-8
# Time    : 2018/10/12 下午10:35
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import VipMember, VipSettings
from main.apps.admin_vip import serializers, filters
from main.common.permissions import PermsRequired


class VipMemberViews(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        返回所有购买会员的用户
    retrieve:
        返回会员用户的详情
    """
    queryset = VipMember.objects.all().order_by('-create_time')
    serializer_class = serializers.VipMemberSerializer
    filter_class = filters.VipMemberFilter
    permission_classes = (PermsRequired('main.vip_info'),)


class VipSettingsViews(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        返回所有的会员配置
    create:
        创建会员权益
    """
    queryset = VipSettings.objects.all()
    serializer_class = serializers.VipSettingsSerializer
    permission_classes = (PermsRequired('main.vip_info'),)

    def perform_create(self, serializer):
        serializer.save(operator_name=self.request.user.staffprofile)

    def perform_update(self, serializer):
        serializer.save(operator_name=self.request.user.staffprofile)
