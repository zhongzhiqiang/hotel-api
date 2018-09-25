# coding:utf-8

from rest_framework import serializers

from main.models import Hotel, RoomStyles


class ImageFiled(serializers.CharField):
    def to_representation(self, value):
        if isinstance(value, basestring):
            return eval(value)
        return value


class TagsField(serializers.CharField):
    def to_representation(self, value):
        if isinstance(value, basestring):
            return eval(value)
        return value


class HotelSerializers(serializers.ModelSerializer):
    address = serializers.CharField(read_only=True)
    tags = serializers.CharField(read_only=True)

    class Meta:
        model = Hotel
        fields = (
            'id',
            'name',
            'address',
            'province',
            'city',
            'area',
            'street',
            'longitude',
            'latitude',
            'cover_images',
            'hotel_profile',
            'min_price',
            'tel',
            'tags'
        )


class RoomStyleSerializer(serializers.ModelSerializer):
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )
    images = ImageFiled()
    tags = serializers.CharField(read_only=True)

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'belong_hotel_name',
            'belong_hotel',
            'room_count',
            'style_name',
            'price',
            'images',
            'room_profile',
            'cover_image',
        )


class HotelDetailSerializer(serializers.ModelSerializer):
    room_styles = RoomStyleSerializer(many=True)

    class Meta:
        model = Hotel
        fields = (
            'id',
            'name',
            'address',
            'province',
            'city',
            'area',
            'street',
            'longitude',
            'latitude',
            'cover_images',
            'hotel_profile',
            'min_price',
            'tel',
            'room_styles',
            'tags'
        )
