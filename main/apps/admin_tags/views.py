# coding:utf-8
# Time    : 2018/9/26 下午9:02
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import viewsets, mixins

from main.apps.admin_tags import serializers
from main.models import Tags


class TagViews(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               viewsets.GenericViewSet):
    """
    create:
        创建tags
    update:
        更新tags.
    list：
        返回所有的tags
    """

    serializer_class = serializers.TagSerializer
    queryset = Tags.objects.all()
