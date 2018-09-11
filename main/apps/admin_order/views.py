# coding:utf-8
# Time    : 2018/8/28 下午9:35
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from main.models import HotelOrder, HotelOrderRoomInfo
from main.apps.admin_order import serializers, filters


class AdminHotelOrderInfoView(mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    """
    list:
        返回所有订单信息
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
    """

    queryset = HotelOrder.objects.prefetch_related('hotel_order_detail', 'hotel_order_room_info')
    serializer_class = serializers.HotelOrderInfoSerializer
    filter_class = filters.HotelOrderFilter

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.HotelOrderSerializer
        elif self.action == 'order_room_info':
            return serializers.HotelOrderRoomInfoSerializer
        elif self.action == 'add_order_room_info':
            return serializers.CreateHotelOrderRoomInfoSerializer
        return self.serializer_class

    @detail_route(methods=['GET'])
    def order_room_info(self, request, *args, **kwargs):
        instance = self.get_object()

        hotel_order_room_info = HotelOrderRoomInfo.objects.filter(belong_order=instance)
        serializer = self.get_serializer(hotel_order_room_info, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def add_order_room_info(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        data.update({"belong_order": instance.order_id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # @detail_route(methods=['POST'])
    # def check_out_room(self, request, *args, **kwargs):
    #     # 退房操作。传递退房房间号。
    #     instance = self.get_object()
    #     data = request.data
    #     data.update({"belong_order": instance.order_id})
