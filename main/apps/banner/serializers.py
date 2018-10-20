# coding:utf-8
# Time    : 2018/9/1 下午4:34
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
        fields = (
            'id',
            'banner_title',
            'banner_images',
            'jump_url'
        )


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = (
            "id",
            "content"
        )