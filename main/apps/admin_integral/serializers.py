# coding:utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Integral, IntegralSettings, GrowthValueSettings, IntegralDetail


class IntegralSerializers(serializers.ModelSerializer):
    class Meta:
        model = Integral
        fields = "__all__"


class IntegralDetailSerializer(serializers.ModelSerializer):
    consumer_name = serializers.CharField(
        source='consumer.user_name',
        read_only=True,
        default='',
        allow_blank=True
    )

    class Meta:
        model = IntegralDetail
        fields = (
            'id',
            'consumer',
            'consumer_name',
            'integral',
            'remark',
            'create_time',
            'left_integral'

        )


class IntegralSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegralSettings
        fields = "__all__"
        read_only_fields = ("operator_name", )


class GrowthValueSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrowthValueSettings
        fields = "__all__"
