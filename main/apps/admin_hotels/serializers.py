# coding:utf-8
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from main.models import Hotel, RoomStyles, Rooms
from main.common.gaode import GaoDeMap
from main.common.seriliazer_fields import ImageField, TagsField


class HotelSerializers(serializers.ModelSerializer):

    address = serializers.CharField(read_only=True)
    tags = serializers.ListField()
    images = serializers.ListField()

    def update(self, instance, validated_data):
        instance = super(HotelSerializers, self).update(instance, validated_data)
        ret = GaoDeMap().get_lat_longitude(instance.address)
        if ret['status'] == '00000':
            instance.longitude = ret['data'].get('longitude')
            instance.latitude = ret['data'].get('latitude')
            instance.save()
        return instance

    class Meta:
        model = Hotel
        fields = (
            'id',
            'name',
            'province',
            'city',
            'area',
            'street',
            'address',
            'longitude',
            'latitude',
            'hotel_profile',
            'cover_images',
            'is_active',
            'create_time',
            'update_time',
            'tel',
            'tags',
            'images',
        )
        read_only_fields = ('longitude', 'latitude')


class AddressSerializers(serializers.Serializer):

    address = serializers.CharField(required=True)


class CreateHotelSerializers(serializers.ModelSerializer):

    tags = serializers.ListField(child=serializers.CharField(max_length=20))
    images = serializers.ListField()

    def validate(self, attrs):

        tags = attrs.get('tags', [])
        if not isinstance(tags, list):
            return serializers.ValidationError({"tags": 'tags须为数组'})
        return attrs

    def create(self, validated_data):
        instance = super(CreateHotelSerializers, self).create(validated_data)
        ret = GaoDeMap().get_lat_longitude(instance.address)
        if ret['status'] == '00000':
            instance.longitude = ret['data'].get('longitude')
            instance.latitude = ret['data'].get('latitude')
            instance.save()
        return instance

    class Meta:
        model = Hotel
        fields = (
            'name',
            'province',
            'city',
            'area',
            'street',
            'hotel_profile',
            'cover_images',
            'tel',
            'tags',
            'is_active',
            'images',
            'longitude',
            'latitude',
            'create_time',
            'update_time',
        )
        read_only_fields = ('longitude', 'latitude')


class CreateRoomStyleSerializer(serializers.ModelSerializer):

    hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )
    images = serializers.ListField(child=serializers.CharField(max_length=300))
    tags = serializers.ListField(child=serializers.CharField(max_length=20))

    def validate_images(self, attr):
        if isinstance(attr, list):
            for i in attr:
                if not i.startswith(("https", "http")):
                    raise serializers.ValidationError("图片路径以http/https开头")
            return attr
        raise serializers.ValidationError("请传递数组")

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'belong_hotel',
            'hotel_name',
            'style_name',
            'price',
            'room_profile',
            'images',
            'cover_image',
            'is_active',
            'room_count',
            'tags'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=RoomStyles.objects.all(),
                fields=('belong_hotel', 'style_name'),
                message='已存在相同类型房间'
            )
        ]


class RoomStyleSerializer(serializers.ModelSerializer):
    images = ImageField()
    tags = TagsField()
    hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'style_name',
            'belong_hotel',
            'price',
            'room_profile',
            'room_count',
            'is_active',
            'images',
            'cover_image',
            'update_time',
            'operator_name',
            'tags',
            'hotel_name'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=RoomStyles.objects.all(),
                fields=('belong_hotel', 'style_name'),
                message='已存在相同类型房间'
            )
        ]


class CreateRoomSerializer(serializers.ModelSerializer):
    style_name = serializers.CharField(
        source='room_style.style_name',
        read_only=True
    )

    class Meta:
        model = Rooms
        fields = (
            'style_name',
            'room_nums',
            'room_style'
        )


class RoomSerializer(serializers.ModelSerializer):
    style_name = serializers.CharField(
        source='room_style.style_name',
        read_only=True
    )
    room_status_display = serializers.CharField(
        source='get_room_status_display',
        read_only=True
    )

    class Meta:
        model = Rooms
        fields = (
            'room_style',
            'style_name',
            'room_nums',
            'room_status',
            'room_status_display',
            'reserve_time',
            'reserve_out_time'
        )
