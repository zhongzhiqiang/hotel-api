# coding:utf-8
# Time    : 2018/8/28 下午4:35
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.admin_banner import serializers
from main.models import Banners


class AdminBannerView(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    queryset = Banners.objects.all()
    serializer_class = serializers.BannerSerializer
