# coding:utf-8

from rest_framework import serializers

from main.models import Hotel


class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"
