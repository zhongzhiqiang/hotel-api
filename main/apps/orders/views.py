# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from main.apps.orders import serializers, filters
from main.models import Order
from main.common.defines import PayType, OrderType, OrderStatus
from main.apps.wx_pay.utils import unifiedorder


class OrderViews(mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """
    create:
        创建住宿订单
    ```
     ORDER_STATUS = (
        (10, '待支付'),
        (15, '待发货'),
        (20, '待收货')
        (25, '待入住'),
        (30, '入住中'),
        (35, '完成待评价'),
        (40, '完成并且已评价'),
        (45, '取消'),
        (50, '待退款'),
        (55, '退款中'),
        (60, '已退款'),
        (65, '已过期')
    )
    PAY_TYPE = (
        (20, '余额'),
        (30, '微信支付')
    )
    {
        "pay_type": "string",  # 支付方式
        "belong_hotel": "string",
        "hotel_order_detail": {
        "room_style": "",  # 传递room_tyle的ID
        "room_nums":""  # 传递需要的房间数,
        "reserve_check_in_time" # 预定入住时间
        "reserve_check_out_time": # 预定退房时间
        "contact_name":"" #联系人
        "contact_phone": "" # 联系电话
        },
        "user_remark": "" # 用户备注
    }
    ```
    list:
        返回所有当前用户订单
        order_express = {
        "express_id": "快递单号",
        "express_name: "快递名称"
        }
    market_order_create:
        创建商场订单
        ```
        PAY_TYPE = (
        (20, '余额'),
        (30, '微信支付')
    )
    
        ORDER_STATUS = (
        (10, '待支付'),
        (15, '待发货'),
        (20, '待收货')
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
        {
        "market_order_detail": [{
        "goods": "",  # 购买商品
        "nums": "",  # 购买数量 
        }],
        "pay_type": "string",  # 支付方式
        "user_remark": "string",  # 用户备注
        "market_order_contact": {
            "consignee_name": # 收货人姓名
            "consignee_address": "收货人地址",
            "consignee_phone": "收货人电话"  
        }
        }
    ```
    refunded:
        退款接口，传递退款状态:order_status=50

    """
    queryset = Order.objects.all().order_by('-create_time')
    serializer_class = serializers.OrderSerializer
    filter_class = filters.HotelOrderFilter
    ordering_fields = ('create_time', 'pay_time', 'order_id')

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateHotelOrderSerializer
        elif self.action == 'market_order_create':
            return serializers.CreateMarketOrderSerializer
        elif self.action == 'refunded':
            return serializers.RefundedOrderSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        if data['pay_type'] == PayType.weixin:
            detail = data['hotel_order_detail']['room_style_name']
            result = unifiedorder('曼嘉酒店-住宿', data['order_id'], data['order_amount'], self.request.user.consumer.openid, detail)
            data.update(result)

        if data['pay_type'] != PayType.weixin and data['order_status'] == 10:
            data.update({"error_message": "余额不足或积分不足,请更换支付方式或者充值"})

        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)

    @list_route(methods=['POST'])
    def market_order_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.data
        if data['pay_type'] == PayType.weixin:

            result = unifiedorder('曼嘉尔酒店-商场', data['order_id'], data['order_amount'], self.request.user.consumer.openid,
                                  '购买商品')
            data.update(result)
        if data['pay_type'] != PayType.weixin and data['order_status'] == 10:
            data.update({"error_message": "余额不足或积分不足,请更换支付方式或者充值"})
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @detail_route(methods=['POST'])
    def refunded(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderPayView(viewsets.GenericViewSet):
    """
    again_pay:
        重新支付。传递支付类型。根据支付类型进行支付
    """
    serializer_class = serializers.OrderPayAgainSerializer
    queryset = Order.objects.all()
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
        if data['pay_type'] == PayType.weixin and data['order_status'] == OrderStatus.pre_pay and data['order_type'] == OrderType.hotel:
            detail = data['hotel_order_detail']['room_style_name']
            result = unifiedorder('曼嘉酒店-住宿', data['order_id'], data['order_amount'], self.request.user.consumer.openid,
                                  detail)
            data.update(result)
        elif data['pay_type'] == PayType.weixin and data['order_status'] == OrderStatus.pre_pay and data['order_type'] == OrderType.market:
            result = unifiedorder('曼嘉酒店-商场', data['order_id'], data['order_amount'], self.request.user.consumer.openid,
                                  '购买商品')
            data.update(result)

        if data['pay_type'] != PayType.weixin and data['order_status'] == 10:
            data.update({"error_message": "余额不足或积分不足,请更换支付方式或者充值"})

        return Response(data)
