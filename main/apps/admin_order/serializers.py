# coding:utf-8
# Time    : 2018/8/23 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import logging

from rest_framework import serializers
from django.db import transaction

from main.models import Order, HotelOrderDetail
from main.apps.admin_integral.utils import get_integral, make_integral

logger = logging.getLogger(__name__)


class HotelOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'belong_order',
            'room_style',
            'room_nums'
        )


class HotelOrderInfoSerializer(serializers.ModelSerializer):
    hotelorderdetail = HotelOrderDetailSerializer(read_only=True)

    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )

    @staticmethod
    def make_integral(instance):
        integral = get_integral(instance.sale_price)
        remark = "住宿:%s,积分:%s" % (instance.hotelorderdetail.room_style.style_name, integral)
        make_integral(instance.consumer, integral, remark)

    def validate(self, attrs):
        order_status = attrs.get("order_status")
        if order_status and order_status < self.instance.order_status:
            raise serializers.ValidationError("当前订单状态为:{}".format(self.instance.get_order_status_display()))
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        order_status = validated_data.get("order_status")

        if order_status == 40 and instance.order_status < 40:
            try:
                self.make_integral(instance)
            except Exception as e:
                logger.warning("make integral error:{}".format(e), exc_info=True)
                raise serializers.ValidationError("生成积分失败")
            validated_data.update({"order_status": 50})
        instance = super(HotelOrderInfoSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = HotelOrder
        fields = (
            'id',
            'belong_hotel',
            'order_id',
            'order_status',
            'order_status_display',
            'room_style_num',
            'sale_price',
            'reserve_check_in_time',
            'reserve_check_out_time',
            'pay_time',
            'create_time',
            'consumer',
            'user_remark',
            'operator_name',
            'flow_remark',
            'hotelorderdetail',
            'contact_name',
            'contact_phone'
        )
        read_only_fields = ('belong_hotel', 'order_id', 'room_style_num',
                            'sale_price', 'reserve_check_in_time',
                            'reserve_check_out_time', 'pay_time', 'consumer',
                            'user_remark', 'operator_name', 'contact_phone',
                            'contact_name')

