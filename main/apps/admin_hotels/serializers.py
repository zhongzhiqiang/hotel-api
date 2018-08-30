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
    hotel = serializers.CharField(
        source='belong_hotel.name'
    )
    images = serializers.ListField(child=serializers.CharField(max_length=300))

    def validate_images(self, attr):
        if isinstance(attr, list):
            for i in attr:
                if not i.startswith(("https", "http")):
                    raise serializers.ValidationError("图片路径以http/https开头")
            return attr
        raise serializers.ValidationError("请传递数组")

    def validate(self, attrs):
        belong_hotel = attrs.pop("belong_hotel", {})
        if belong_hotel:
            hotel = Hotel.objects.filter(name=belong_hotel.get("name")).first()
            if not hotel:
                raise serializers.ValidationError("请正确填写宾馆名称")
            attrs.update({"belong_hotel": hotel})
        return attrs

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'hotel',
            'style_name',
            'price',
            'room_profile',
            'images',
            'is_active'
        )


class RoomStyleSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.CharField(max_length=300), read_only=False)

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'style_name',
            'room_profile',
            'room_count',
            'is_active',
            'left_room_count',
            'images',
        )
        read_only_fields = ('room_count', 'left_room_count')


class CreateRoomSerializer(serializers.ModelSerializer):
    style_name = serializers.CharField(
        source='room_style.style_name',
    )

    def validate(self, attrs):

        style_name = attrs.pop('room_style', {}).get('style_name')
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
        source='room_style.style_name'
    )
    room_status_display = serializers.CharField(
        source='get_room_status_display',
        read_only=True
    )

    def validate(self, attrs):
        style_name = attrs.pop('room_style', {}).get('style_name')
        if style_name:
            room_style = RoomStyles.objects.filter(style_name=style_name).first()
            if not room_style:
                raise serializers.ValidationError("请正确房间类型名称")
            attrs.update({"room_style": room_style})
        return attrs

    class Meta:
        model = Rooms
        fields = (
            'room_style',
            'room_nums',
            'room_status',
            'room_status_display',
            'reserve_time',
            'reserve_out_time'
        )
