# coding:utf-8
# Time    : 2018/8/23 下午9:25
# Author  : Zhongzq
# Site    : 
# File    : serializer.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import IntegralDetail, IntegralInfo


class IntegralDetailSerializer(serializers.ModelSerializer):

    consumer_name = serializers.CharField(
        source='consumer.user_name',
        read_only=True
    )
    integral_type_display = serializers.CharField(
        source='get_integral_type_display',
        read_only=True
    )

    class Meta:
        model = IntegralDetail
        fields = (
            'id',
            'consumer',
            'consumer_name',
            'integral_type',
            'integral_type_display',
            'remark',
            'create_time',
            'left_integral'
        )


class IntegralSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegralInfo
        fields = "__all__"
