# coding:utf-8
# Time    : 2018/9/1 下午1:53
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import Banners
from main.apps.banner import serializers


class BannerViews(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    list:
        返回所有的banner
    """
    queryset = Banners.objects.filter(is_show=True)
    serializer_class = serializers.BannerSerializer
