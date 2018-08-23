# coding:utf-8
# Time    : 2018/8/23 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import HotelOrder, HotelOrderDetail, HotelOrderRoomInfo


class HotelOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'belong_order',
            'room_style',
            'room_style_name',
            'room_nums'
        )


class HotelOrderSerializer(serializers.ModelSerializer):
    hotel_order_detail = HotelOrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = HotelOrder
        fields = "__all__"


class CreateHotelOrderRoomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrderRoomInfo
        fields = (
            'belong_order',
            'guest_info',
            'check_in_room'
        )
