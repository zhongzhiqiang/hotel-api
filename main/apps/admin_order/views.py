# coding:utf-8
# Time    : 2018/8/28 下午9:35
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import Order
from main.apps.admin_order import serializers, filters
from main.common.defines import OrderType


class AdminHotelOrderInfoView(mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    list:
        返回所有订单信息
        ORDER_STATUS = (
        (10, '待支付'),
        (25, '待入住'),
        (30, '入住中'),
        (35, '完成待评价'),
        (40, '完成并且已评价'),
        (45, '取消'),
        (50, '待退款'),
        (55, '退款中'),
        (69, '已退款'),
        (65, '已过期')
        )
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建数据
    retrieve:
        返回订单详细信息
    order_room_info:
        返回订单入住的房间信息以及客户信息
    add_order_room_info:
        添加用户入住信息。
        ```
        用户信息列表
        guest_info = [{"idcard_name":"123", "idcard_num":"123"}]
        传递数据:
        data = {
            "c"
        }
        ```
    refund:
        退款。
    """

    queryset = Order.objects.filter(order_type=OrderType.hotel).prefetch_related('hotel_order_detail', 'order_pay')
    serializer_class = serializers.HotelOrderInfoSerializer
    filter_class = filters.HotelOrderFilter

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.HotelOrderInfoSerializer
        return self.serializer_class
