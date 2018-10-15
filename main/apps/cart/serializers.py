# coding:utf-8
# Time    : 2018/10/15 下午10:26
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Cart


class CartListSerializers(serializers.ListSerializer):
    def create(self, validated_data):
        cart_list = [Cart(**item) for item in validated_data]
        return Cart.objects.bulk_create(cart_list)


class CartSerializers(serializers.ModelSerializer):

    goods_price = serializers.CharField(
        source='goods.goods_price',
        read_only=True
    )

    goods_integral = serializers.CharField(
        source='goods.need_integral',
        read_only=True
    )
    is_integral = serializers.CharField(
        source='goods.is_integral',
        read_only=True
    )

    def validate(self, attrs):
        goods = attrs.get("goods")
        if not goods:
            raise serializers.ValidationError("请传递商品")

        return attrs

    class Meta:
        model = Cart
        list_serializer_class = CartListSerializers
        fields = (
            'id',
            'goods',
            'nums',
            'goods_price',
            'goods_integral',
            'is_integral'
        )


