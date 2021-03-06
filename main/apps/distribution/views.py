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
from main.common.permissions import ClientPermission


class DistributionApplyView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
        create:
            申请成为分销人员
            ```
                APPLY_STATUS = (
        (10, '提交成功'),
        (20, '拒绝'),
        (30, '完成'),
        (40, '撤回申请'),
    )
            ```
        list:
            返回分销申请列表
        retrieve:
            返回单个申请详情
        update:
            更新申请
    """
    queryset = DistributionApply.objects.all()  # 这里需要根据用户来返回
    serializer_class = serializers.ApplySerializer
    permission_classes = (ClientPermission, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.consumer)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateApplySerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)


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
    permission_classes = (ClientPermission, )

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)


class DistributionBonusPickViews(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    """
    create:
        创建分销金额提取
        ```
        PICK_STATUS = (
        (10, '提交申请'),
        (20, '正在处理'),
        (30, '转账中'),
        (40, '完成'),
        (50, '提取失败'),
        (60, '取消申请'),
    )

    TRANSFER_TYPE = (
        (10, '支付宝'),
        (20, '微信'),
        (30, '银行卡'),
    )
        ```
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
    permission_classes = (ClientPermission, )

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateBonusPickSerializer
        return self.serializer_class
