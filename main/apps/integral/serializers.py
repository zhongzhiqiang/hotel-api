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
    class Meta:
        model = IntegralDetail
        fields = "__all__"


class IntegralSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegralInfo
        fields = "__all__"
