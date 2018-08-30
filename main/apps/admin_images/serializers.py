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
    class Meta:
        model = Images
        fields = "__all__"
