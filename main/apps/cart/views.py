# coding:utf-8
# Time    : 2018/10/15 下午10:47
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.cart import serializers
from main.models import Cart


class CartViews(mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializers
