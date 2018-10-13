# coding:utf-8
# Time    : 2018/8/28 下午3:27
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Images


class ImageSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(
        source='operator_name.user_name',
        read_only=True
    )

    class Meta:
        model = Images
        fields = (
            'id',
            'image',
            'operator_name',
            'create_time'
        )


class CreateImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = (
            'id',
            'image',
        )
