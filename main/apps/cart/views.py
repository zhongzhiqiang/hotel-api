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
                mixins.ListModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """
    create:
        在自己的购物车新增一件商品
        如果购物车有一样的商品会合并
    list:
        返回当前用户的购物车
    update:
        更新购物车商品某个商品
    """
    queryset = Cart.objects.all()
    serializer_class = serializers.CartSerializers

    def get_queryset(self):
        return self.queryset.filter(consumer=self.request.user.consumer)

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)
