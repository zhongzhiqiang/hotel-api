# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from main.apps.hotel_orders import serializers
from main.models import HotelOrder
from main.common.defines import PayType
from main.apps.wx_pay.utils import unifiedorder


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        if data['pay_type'] == PayType.weixin:
            detail = data['hotelorderdetail']['room_style_name']
            data = unifiedorder(data['order_id'], data['sale_price'], self.request.user.consumer.openid, detail)
            data.update({"pay_type": PayType.weixin})

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)
