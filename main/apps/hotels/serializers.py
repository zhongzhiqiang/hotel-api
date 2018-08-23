# coding:utf-8

from rest_framework import serializers

from main.models import Hotel, RoomStyles


class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class RoomStyleSerializer(serializers.ModelSerializer):
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'belong_hotel_name',
            'belong_hotel',
            'style_name',
            'price',
            'room_profile'
        )
