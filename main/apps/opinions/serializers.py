# coding:utf-8
# Time    : 2018/11/14 下午10:12
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Opinions


class OpinionsSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if not attrs.get("phone"):
            raise serializers.ValidationError({"请传递手机号"})
        return attrs

    class Meta:
        model = Opinions
        fields = (
            'id',
            'content',
            'create_time',
            'phone'
        )
