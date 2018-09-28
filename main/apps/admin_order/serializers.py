# coding:utf-8
# Time    : 2018/8/23 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import HotelOrder, HotelOrderDetail


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
