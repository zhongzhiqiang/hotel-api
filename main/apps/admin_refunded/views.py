# coding:utf-8
# Time    : 2018/10/20 下午10:25
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route

from main.models import Order
from main.common.defines import OrderType, OrderStatus
from main.apps.admin_refunded import serializers


refund_status = [OrderStatus.pre_refund, OrderStatus.refund_ing, OrderStatus.refunded]


class HotelRefundedViews(mixins.ListModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
        返回当前所有待退款, 退款中, 退款完成, 退款失败的订单.
        WX_REFUND_STATUS = (
        (10, '退款中'),
        (20, '成功'),
        (30, '失败'),
        (40, '重试'),
        (50, '未知')
        )
        ```
        refunded_account 为退款到账时间
        ```
    partial_update:
        退款接口 与put接口二选一
    update:
        退款接口
    retrieve:
        返回详细信息
    
    # 还差微信退款查询接口。已经重新退款接口

    """
    queryset = Order.objects.filter(order_type=OrderType.hotel,
                                    order_status__in=refund_status)
    serializer_class = serializers.HotelOrderRefundedSerializer

    def perform_update(self, serializer):
        serializer.save(consumer=self.request.user.consumer)


class MarketRefundedViews(mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
           返回当前所有待退款, 退款中, 退款完成, 退款失败的订单.
           WX_REFUND_STATUS = (
        (10, '退款中'),
        (20, '成功'),
        (30, '失败'),
        (40, '重试'),
        (50, '未知')
        )
        ```
        refunded_account 为退款到账时间
        ```
    partial_update:
        退款接口 与put接口二选一
    update:
        退款接口
    retrieve:
        返回详细信息

    """
    queryset = Order.objects.filter(order_type=OrderType.market,
                                    order_status__in=refund_status)
    serializer_class = serializers.MarketRefundedSerializer

    def perform_update(self, serializer):
        serializer.save(consumer=self.request.user.consumer)
