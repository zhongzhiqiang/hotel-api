# coding:utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Hotel, RoomStyles, Rooms


class HotelSerializers(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = "__all__"
        read_only_fields = ('longitude', 'latitude')


class AddressSerializers(serializers.Serializer):

    address = serializers.CharField(required=True)


class CreateHotelSerializers(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = (
            'name',
            'address',
            'longitude',
            'latitude',
            'hotel_profile'
        )


class CreateRoomStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomStyles
        fields = "__all__"


class RoomStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'style_name',
            'room_profile',
            'room_count'
            'is_active',
            'left_room_count'
        )
        read_only_fields = ('room_count', 'left_room_count')


class CreateRoomSerializer(serializers.ModelSerializer):
    style_name = serializers.CharField(
        source='room_style.style_name',
    )

    def validate(self, attrs):
        style_name = attrs.pop('style_name', '')
        room_style = RoomStyles.objects.filter(style_name=style_name).first()
        if not room_style:
            raise serializers.ValidationError("请填写房间类型名称")
        attrs.update({"room_style": room_style})
        return attrs

    class Meta:
        model = Rooms
        fields = (
            'style_name',
            'room_nums'
        )


class RoomSerializer(serializers.ModelSerializer):

    room_style = serializers.CharField(
        source='room_style.style_name',
        read_only=True
    )

    class Meta:
        model = Rooms
        fields = (
            'room_style',
            'room_nums',
            'room_status',
            'reserve_time'
            'check_in_time',
            'check_out_time'
        )
