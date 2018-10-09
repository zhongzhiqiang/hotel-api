# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from main.apps.hotel_orders import serializers, filters
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
    list:
        返回所有当前用户订单
        ORDER_STATUS = (
        (10, '未支付'),
        (20, '待发货'),
        (30, '待收货'),
        (40, '已完成'),
        (50, '已取消'),
        (60, '等待评价'),
        (70, '评价完成')  # 评价完成后才有积分
    )
    """
    queryset = HotelOrder.objects.all().order_by('-create_time')
    serializer_class = serializers.HotelOrderSerializer
    filter_class = filters.HotelOrderFilter
    ordering_fields = ('create_time', 'pay_time', 'order_id')

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
            result = unifiedorder('曼嘉酒店-住宿', data['order_id'], data['sale_price'], self.request.user.consumer.openid, detail)

            data.update(result)

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)


class HotelOrderPayView(viewsets.GenericViewSet):
    """
    again_pay:
        重新支付。传递支付类型。根据支付类型进行支付
    """
    serializer_class = serializers.HotelOrderPayAgainSerializer
    queryset = HotelOrder.objects.all()
    lookup_field = 'order_id'

    def perform_update(self, serializer):
        serializer.save()

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)

    @detail_route(methods=['POST'])
    def again_pay(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = serializer.data

        # 支付方式为30，并且状态为10时，重新生成支付信息
        if data['pay_type'] == PayType.weixin and data['order_status'] == 10:
            detail = data['hotelorderdetail']['room_style_name']
            result = unifiedorder('曼嘉酒店-住宿', data['order_id'], data['sale_price'], self.request.user.consumer.openid,
                                  detail)

            data.update(result)
        return Response(data)
