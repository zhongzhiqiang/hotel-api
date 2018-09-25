# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import serializers
from django.db.transaction import atomic

from main.models import HotelOrder, HotelOrderDetail, Hotel


class CreateHotelOrderDetailSerializer(serializers.ModelSerializer):
    room_style = serializers.CharField(
        source='room_style.style_name',
    )

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style',
            'room_nums',
            'room_price',
        )


class CreateHotelOrderSerializer(serializers.ModelSerializer):
    belong_hotel = serializers.CharField(
        source='belong_hotel.name'
    )
    hotel_detail = CreateHotelOrderDetailSerializer()

    @atomic
    def create(self, validated_data):
        hotel_detail = validated_data.pop('hotel_detail', {})
        sale_price = hotel_detail.get('room_nums', 0) * hotel_detail.get('room_price')
        validated_data.update({"sale_price": sale_price})
        instance = super(CreateHotelOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()

        hotel_detail_obj = HotelOrderDetail(belong_order=instance, **hotel_detail)
        hotel_detail_obj.save()
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
        read_only_fields = ('order_id', 'order_status', 'room_style_num', 'sale_price')


class HotelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrder
        fields = "__all__"
