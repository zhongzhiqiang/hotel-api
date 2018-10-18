# coding:utf-8
# Time    : 2018/9/26 下午9:47
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route

from main.apps.admin_marketorder import serializers, filters
from main.models import Order
from main.common.defines import OrderType


class MarketOrderView(mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    list:
        返回所有的信息
        ```
        订单状态对应的数字。
         ORDER_STATUS = (
        (10, '待支付'),
        (15, '待发货'),
        (20, '待收货')
        (35, '待评价'),
        (40, '已评价'),
        (45, '取消'),
        (50, '待退款'),
        (55, '退款中'),
        (69, '已退款'),
        (65, '已过期')
        )
        ```
    update:
        更新状态。
        ```
        order_express = {
        "express_id": "快递单号",
        "express_name": "快递名称",
        }
        ```
    retrieve:
        详情
        ```
         order_express = {
        "express_id": "快递单号",
        "express_name": "快递名称",
        }
        ```
    market_refunded:
        商场订单退款.不需要传递任何参数。
    """
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.filter(
        order_type=OrderType.market).prefetch_related(
        'order_pay', 'order_refunded', 'market_order_detail', 'market_order_detail__goods').order_by('-create_time')
    filter_class = filters.OrderFilter

    def get_serializer_class(self):
        if self.action == 'market_refunded':
            return serializers.RefundedSerializer
        return self.serializer_class

    @detail_route(methods=['POST'])
    def market_refunded(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

