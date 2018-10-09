# coding:utf-8
# Time    : 2018/10/4 下午6:33
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from main.models import RechargeSettings, RechargeInfo
from main.apps.recharge import serializers
from main.apps.wx_pay.utils import unifiedorder


class RechargeSettingsViews(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        返回所有的充值配置
    """
    queryset = RechargeSettings.objects.filter(is_active=True)
    serializer_class = serializers.RechargeSettingsSerializer


class RechargeViews(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    create:
        创建充值信息
        ```
        recharge_money 为配置充值的金额
        ```
            RECHARGE_STATUS = (
        (10, '成功'),
        (20, '取消'),
        (30, '等待支付')
    )
    update:
        更新充值状态，只能够变为取消。
    list:
        返回当前用户的所有充值记录
    """
    queryset = RechargeInfo.objects.all()
    serializer_class = serializers.RechargeSerializer

    def get_queryset(self):
        if hasattr(self.request.user, 'consumer'):
            return self.queryset.filter(consumer=self.request.user.consumer)
        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateRechargeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data

        headers = self.get_success_headers(data)
        result = unifiedorder('曼嘉酒店-充值余额', data['order_id'], data['recharge_money'],
                              self.request.user.consumer.openid, '充值余额')
        data.update(result)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class RechargeAgainPayView(viewsets.GenericViewSet):
    """
    cancel_recharge:
        从等待支付变为取消。已充值无法变为取消
    again_recharge:
        重新支付.
    """

    queryset = RechargeInfo.objects.all()
    serializer_class = serializers.RechargePayAgainSerializer
    lookup_field = 'order_id'

    def get_serializer_class(self):
        if self.action == 'again_recharge':
            return self.serializer_class
        return serializers.RechargeCancelSerializer

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        if hasattr(self.request.user, 'consumer'):
            return self.queryset.filter(consumer=self.request.user.consumer)
        return self.request

    @detail_route(methods=['POST'])
    def cancel_recharge(self, request, *args, **kwargs):
        # 从等待支付变为取消。已充值无法变为取消
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data
        return Response(data)

    @detail_route(methods=['POST'])
    def again_recharge(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data

        if data['recharge_status'] in (20, 30):
            result = unifiedorder('曼嘉酒店-充值余额', data['order_id'], data['recharge_money'],
                                  self.request.user.consumer.openid, '充值余额')
            data.update(result)

        return Response(data)
