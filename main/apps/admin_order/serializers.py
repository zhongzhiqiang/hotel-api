# coding:utf-8
# Time    : 2018/8/23 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import logging
import datetime

from rest_framework import serializers
from django.db import transaction

from main.models import Order, HotelOrderDetail, OrderPay, OrderRefunded
from main.apps.admin_integral.utils import get_integral, make_integral
from main.common.defines import OrderStatus


logger = logging.getLogger('django')


def increase_room_num(order):
    room_style = order.hotel_order_detail.room_style
    room_style.room_count = room_style.room_count + order.hotel_order_detail.room_nums
    room_style.save()


class HotelOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style',
            'room_nums',
            'room_price',
            "reserve_check_in_time",
            "reserve_check_out_time",
            "contact_name",
            "contact_phone",
            "room_style_name",
            "days"
        )


class OrderPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPay
        fields = (
            "id",
            "wx_order_id",
            "free_money",
            "integral",
            "money",
            "create_time"
        )


class OrderRefundedSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRefunded
        fields = "__all__"


class HotelOrderInfoSerializer(serializers.ModelSerializer):
    hotel_order_detail = HotelOrderDetailSerializer(read_only=True)
    order_pay = OrderPaySerializer(read_only=True)

    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True
    )

    order_refunded = OrderRefundedSerializer(read_only=True)

    @staticmethod
    def make_integral(instance):
        integral = get_integral(instance.order_amount)
        remark = "住宿:%s,积分:%s" % (instance.hotel_order_detail.room_style.style_name, integral)
        make_integral(instance.consumer, integral, remark)

    def validate(self, attrs):
        order_status = attrs.get("order_status")
        if order_status and order_status < self.instance.order_status:
            raise serializers.ValidationError("当前订单状态为:{}".format(self.instance.get_order_status_display()))
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        order_status = validated_data.get("order_status")
        validated_data.update({"operator_time": datetime.datetime.now()})
        # 生成积分是，当用户入住完成时
        if order_status == OrderStatus.success and instance.order_status == OrderStatus.check_in:
            try:
                self.make_integral(instance)
            except Exception as e:
                logger.warning("make integral error:{}".format(e), exc_info=True)
                raise serializers.ValidationError("生成积分失败")
            increase_room_num(self.instance)
            validated_data.update({"order_status": OrderStatus.success})
        instance = super(HotelOrderInfoSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = Order
        fields = (
            "id",
            'hotel_order_detail',
            'order_pay',
            "order_id",
            "belong_hotel",
            "belong_hotel_name",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_type",
            "pay_type_display",
            "pay_time",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "operator_name",
            "operator_time",
            "refund_reason",
            "user_remark",
            "operator_remark",
            "order_refunded"
        )
        read_only_fields = (
            "order_id",
            "belong_hotel",
            "pay_type",
            "pay_time",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "operator_name",
            "operator_time",
            "refund_reason",
            "user_remark"
        )


