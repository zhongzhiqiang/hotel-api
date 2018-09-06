# coding:utf-8
# Time    : 2018/8/29 下午10:23
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import mixins, viewsets

from main.models import DistributionApply, DistributionBonusDetail, DistributionBonusPick
from main.apps.distribution import serializers


class DistributionApplyView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
        create:
            申请成为分销人员
        list:
            返回分销申请列表
        retrieve:
            返回单个申请详情
        update:
            更新申请
    """
    queryset = DistributionApply.objects.all()  # 这里需要根据用户来返回
    serializer_class = serializers.ApplySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.consumer)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateApplySerializer
        return self.serializer_class


class DistributionDetailView(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
        list:
            返回当前用户的奖金列表
        retrieve:
            返回详细的数据
    """
    queryset = DistributionBonusDetail.objects.all()
    serializer_class = serializers.DistributionBonusDetailSerializer


class DistributionBonusPickViews(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    """
    create:
        创建分销金额提取
    update:
        更新分销金额提取.传递pick_order值
    retrieve:
        返回提取明细,传递pick_order值
    list:
        返回所有的分销金额提取
    """
    queryset = DistributionBonusPick.objects.all()
    serializer_class = serializers.BonusPickSerializer
    lookup_field = 'pick_order'

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateBonusPickSerializer
        return self.serializer_class
