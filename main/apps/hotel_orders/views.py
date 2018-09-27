# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.hotel_orders import serializers
from main.models import HotelOrder


class HotelOrderViews(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    create:
        创建订单
    ```
    {
        "pay_type": "string",
        "belong_hotel": "string",
        "hotelorderdetail": {
        "room_style": "",  # 传递room_tyle的ID
        "room_nums":""  # 传递需要的房间数
        },
        "reserve_check_out_time": "string",  # 退房时间
        "user_remark": "string",
        "reserve_check_in_time": "string"  # 入住时间
    }
    ```
    """
    queryset = HotelOrder.objects.all()
    serializer_class = serializers.HotelOrderSerializer

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateHotelOrderSerializer
        return self.serializer_class
