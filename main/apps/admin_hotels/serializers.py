# coding:utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Hotel


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
