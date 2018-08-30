# coding:utf-8
# Time    : 2018/8/23 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import HotelOrder, HotelOrderDetail, HotelOrderRoomInfo, Rooms


class GuestInfoSerializer(serializers.Serializer):
    idcard_name = serializers.CharField(max_length=30)
    idcard_num = serializers.CharField(max_length=30)


class HotelOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'belong_order',
            'room_style',
            'room_nums'
        )


class HotelOrderRoomInfoSerializer(serializers.ModelSerializer):
    guest_info = serializers.ListField(child=GuestInfoSerializer())
    check_in_room_num = serializers.CharField(
        source='check_in_room.room_nums'
    )

    class Meta:
        model = HotelOrderRoomInfo
        fields = (
            'id',
            'belong_order',
            'guest_info',
            'check_in_room',
            'check_in_room_num'
        )


class HotelOrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrder
        fields = "__all__"


class HotelOrderSerializer(serializers.ModelSerializer):
    hotel_order_detail = HotelOrderDetailSerializer(many=True, read_only=True)
    hotel_order_room_info = HotelOrderRoomInfoSerializer(many=True, read_only=True)

    class Meta:
        model = HotelOrder
        fields = "__all__"


# class GuestInfoListSerializer(serializers.ListField):
#     idcard_name = serializers.CharField(max_length=30)
#     idcard_num = serializers.CharField(max_length=30)


class CheckOutRoomSerializer(serializers.ModelSerializer):
    belong_order = serializers.CharField(
        source='belong_order.order_id',
    )
    check_in_room = serializers.CharField(
        source='check_in_room.room_nums'
    )

    def validate(self, attrs):
        belong_order = attrs.pop('belong_order', {})
        check_in_room = attrs.pop('check_in_room', {})
        belong_order_order_id = belong_order.get("order_id")
        # hotel_order = HotelOrder.objects.filter(order_id=belong_order_order_id).first()
        hotel_order = HotelOrder.objects.get(order_id=belong_order_order_id)
        if belong_order and not hotel_order:
            raise serializers.ValidationError("请输入正确的订单号")
        room_nums = check_in_room.get('room_nums')
        room_info = Rooms.objects.filter(room_nums=room_nums).first()
        if check_in_room and not room_info:
            raise serializers.ValidationError("请输入正确的房间号")
        room = hotel_order.hotel_order_room_info.filter(check_in_room=room_info).first()
        if not room:
            raise serializers.ValidationError({""})
        attrs.update({"belong_order": hotel_order})
        attrs.update({"check_in_room": room_info})
        return attrs

    class Meta:
        model = HotelOrderRoomInfo
        fields = (
            'id',
            'belong_order',
            'check_out_time',
            'check_in_room'
        )


class CreateHotelOrderRoomInfoSerializer(serializers.ModelSerializer):
    guest_info = serializers.ListField(child=GuestInfoSerializer())

    belong_order = serializers.CharField(
        source='belong_order.order_id'
    )
    check_in_room = serializers.CharField(
        source='check_in_room.room_nums'
    )

    def validate(self, attrs):
        belong_order = attrs.pop('belong_order', {})
        check_in_room = attrs.pop('check_in_room', {})
        belong_order_order_id = belong_order.get("order_id")
        hotel_order = HotelOrder.objects.filter(order_id=belong_order_order_id).first()
        if belong_order and not hotel_order:
            raise serializers.ValidationError("请输入正确的订单号")
        room_nums = check_in_room.get('room_nums')
        room_info = Rooms.objects.filter(room_nums=room_nums).first()
        if check_in_room and not room_info:
            raise serializers.ValidationError("请输入正确的房间号")
        attrs.update({"belong_order": hotel_order})
        attrs.update({"check_in_room": room_info})
        return attrs

    class Meta:
        model = HotelOrderRoomInfo
        fields = (
            'id',
            'belong_order',
            'guest_info',
            'check_in_room'
        )
