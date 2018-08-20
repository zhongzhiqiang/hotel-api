# coding:utf-8
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from main.models import GrowthValueSettings, Integral, IntegralDetail
from main.apps.admin_integral import serializers


class GrowthValueSettingView(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    # 成长值配置
    queryset = GrowthValueSettings.objects.all()
    serializer_class = serializers.GrowthValueSettingsSerializer


class UserIntegralView(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    queryset = Integral.objects.all()
    serializer_class = serializers.IntegralSerializers

    def retrieve(self, request, *args, **kwargs):
        # 返回用户的积分详情

        instance = self.get_object()
        user = instance.user
        data = IntegralDetail.objects.filter(consumer=user)
        serializer = serializers.IntegralDetailSerializer(data, many=True)
        return Response(serializer.data)
