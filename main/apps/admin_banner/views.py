# coding:utf-8
# Time    : 2018/8/28 下午4:35
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.admin_banner import serializers, filters
from main.models import Banners


class AdminBannerView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    create:
        创建横幅
    update:
        更新横幅
    list:
        返回所有横幅
    retrieve:
        返回横幅详情
    """
    def perform_create(self, serializer):
        if self.request.user and self.request.user.staffprofile:
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user and self.request.user.staffprofile:
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    queryset = Banners.objects.all()
    serializer_class = serializers.BannerSerializer
    filter_class = filters.BannersFilter
