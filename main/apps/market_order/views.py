# coding:utf-8
# Time    : 2018/9/8 下午8:27
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from main.apps.market_order import serializers
from main.apps.wx_pay.utils import unifiedorder
from main.common.defines import PayType
from main.common.permissions import ClientPermission
from main.models import MarketOrder


class MarketOrderViews(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        返回当前用户的所有订单.
        ```
        ORDER_STATUS = (
        (10, '未支付'),
        (20, '待发货'),
        (30, '待收货'),
        (40, '已完成'),
        (50, '已取消'),
        (60, '等待评价'),
        (70, '评价完成')  # 评价完成后才有积分
    )
        ```
    create:
        创建订单
        ```
        market_order_detail 字段传递:
        {"goods":"商品id，从goods获取的id"，  
        "nums"： "购买数量"}
        ```
    update:
        更新数据。
    """
    queryset = MarketOrder.objects.filter().prefetch_related('marketorderdetail').prefetch_related('marketorderdetail__goods')
    serializer_class = serializers.MarketOrderSerializer
    permission_classes = (ClientPermission, )

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)
        return serializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateMarketOrderSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.request.user and hasattr(self.request.user, 'consumer'):
            return self.queryset.filter(consumer=self.request.user.consumer)
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.data
        if data['pay_type'] == PayType.weixin:
            detail = data['marketorderdetail']['goods_name']
            result = unifiedorder('曼嘉尔酒店-商场', data['order_id'], data['pay_money'], self.request.user.consumer.openid, detail)
            data.update(result)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
