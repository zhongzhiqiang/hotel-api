# coding:utf-8
# Time    : 2018/10/15 下午10:47
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from main.apps.cart import serializers
from main.models import Cart


class CartViews(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """
    create:
        在自己的购物车新增一件商品
        如果购物车有一样的商品会合并.如果传递数字小于等于0 则会删除
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

    def create(self, request, *args, **kwargs):
        post_data = request.data
        if post_data.get("nums") <= 0:
            cart = self.queryset.filter(goods__id=post_data.get("goods")).first()
            if cart:
                cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"non_field_errors": "传递错误"})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)