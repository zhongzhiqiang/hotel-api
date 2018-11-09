# coding:utf-8
# Time    : 2018/8/30 下午8:44
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import DistributionApply, DistributionBonusPick
from main.apps.admin_distribution import serializers, filters
from main.common.permissions import PermsRequired


class AdminDistributionApplyView(mixins.UpdateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    """
        update:
            更新分销人员申请
        list:
            返回所有申请列表
        retrieve:
            返回单个申请详情
    """

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    queryset = DistributionApply.objects.all()
    serializer_class = serializers.ApplySerializer
    search_fields = ("consumer__user_name", )
    filter_class = filters.ApplyFilter
    permission_classes = (PermsRequired('main.distribution'), )


class BonusPickViews(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    update:
        更新提取状态等。
    list:
        返回所有的提取记录
    retrieve:
        返回提取记录详情
    """
    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    queryset = DistributionBonusPick.objects.all()
    serializer_class = serializers.BonusPickSerializer
    filter_class = filters.PickFilter
