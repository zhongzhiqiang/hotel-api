# coding:utf-8
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from main.models import GrowthValueSettings, Integral, IntegralDetail, IntegralSettings
from main.apps.admin_integral import serializers


class GrowthValueSettingView(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    list:
        返回成长值配置
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建数据
    retrieve:
        返回单个数据。查询id为list返回的id
    """

    def perform_create(self, serializer):
        if self.request.user and self.request.user.staffprofile:
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user and self.request.user.staffprofile:
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()
    # 成长值配置
    queryset = GrowthValueSettings.objects.all()
    serializer_class = serializers.GrowthValueSettingsSerializer


class AdminIntegralSettingsView(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    list：
        返回所有积分配置
    partial_update:
        更新积分配置部分字段
    update:
        更新积分配置
    create:
        创建积分配置
    """

    def perform_create(self, serializer):
        if self.request.user and self.request.user.staffprofile:
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user and self.request.user.staffprofile:
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    queryset = IntegralSettings.objects.all()
    serializer_class = serializers.IntegralSettingsSerializer


class UserIntegralView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        返回所有用户的积分
    retrieve:
        返回用户的积分详情数据。查询id为list返回的id
    """
    queryset = Integral.objects.all()
    serializer_class = serializers.IntegralSerializers

    def retrieve(self, request, *args, **kwargs):
        # 返回用户的积分详情
        instance = self.get_object()
        user = instance.user
        data = IntegralDetail.objects.filter(consumer=user)
        serializer = serializers.IntegralDetailSerializer(data, many=True)
        return Response(serializer.data)
