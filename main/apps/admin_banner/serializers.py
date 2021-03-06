# coding:utf-8
# Time    : 2018/8/28 下午4:34
# Author  : Zhongzq
# Site    : 
# File    : serializer.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Banners, Notice


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = "__all__"


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"
        read_only_fields = ("operator_name", )
