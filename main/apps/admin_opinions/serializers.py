# coding:utf-8
# Time    : 2018/11/14 下午10:08
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Opinions


class OpinionsSerializers(serializers.ModelSerializer):
    consumer_name = serializers.CharField(
        source='consumer.user_name',
        read_only=True
    )

    class Meta:
        model = Opinions
        fields = (
            'id',
            'consumer_name',
            'consumer',
            'content',
            'create_time',
            'phone'
        )
