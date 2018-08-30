# coding:utf-8
# Time    : 2018/8/28 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import Images
from main.apps.admin_images import serializers


class ImageViews(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):

    queryset = Images.objects.all()
    serializer_class = serializers.ImageSerializer
