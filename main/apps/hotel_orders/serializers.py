# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import serializers

from main.models import HotelOrder, HotelOrderDetail, HotelOrderRoomInfo


class CreateHotelOrderDetailSerializer(serializers.ModelSerializer):
    room_style = serializers.CharField(
        source='room_style.style_name',
    )

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style',
            'room_nms',
            'room_price',
        )


class CreateHotelOrderSerializer(serializers.ModelSerializer):
    belong_hotel = serializers.CharField(
        source='belong_hotel.name'
    )
    hotel_detail = CreateHotelOrderDetailSerializer(many=True)

    def create(self, validated_data):
        instance = super(CreateHotelOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        return instance

    class Meta:
        model = HotelOrder
        fields = (
            'id',
            'order_id',
            'order_status',
            'room_style_num',
            'sale_price',
            'reserve_check_in_time',
            'reserve_check_out_time',
            'user_remark',
            'belong_hotel',
            'hotel_detail'
        )
