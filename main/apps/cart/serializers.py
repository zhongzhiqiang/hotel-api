# coding:utf-8
# Time    : 2018/10/15 下午10:26
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from django.db import transaction

from main.models import Cart


class CartSerializers(serializers.ModelSerializer):
    goods_price = serializers.CharField(
        source='goods.goods_price',
        read_only=True
    )

    goods_integral = serializers.CharField(
        source='goods.need_integral',
        read_only=True
    )
    is_integral = serializers.BooleanField(
        source='goods.is_integral',
        read_only=True
    )
    cart_id = serializers.CharField(
        source='id',
        read_only=True
    )
    id = serializers.CharField(
        source='goods.id',
        read_only=True
    )
    goods_name = serializers.CharField(
        source='goods.goods_name',
        read_only=True
    )
    cover_image = serializers.CharField(
        source='goods.cover_image',
        read_only=True
    )

    def validate(self, attrs):
        goods = attrs.get("goods")
        if not goods:
            raise serializers.ValidationError("请传递商品")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        consumer = self.context['request'].user.consumer
        goods = validated_data.get('goods')
        instance = Cart.objects.filter(consumer=consumer, goods=goods).first()
        if instance:
            instance.nums = validated_data['nums']
            instance.save()
            return instance
        else:
            instance = super(CartSerializers, self).create(validated_data)

        return instance

    class Meta:
        model = Cart
        fields = (
            'id',
            'cart_id',
            'goods',
            'nums',
            'goods_price',
            'goods_integral',
            'is_integral',
            'goods_name',
            'cover_image'
        )

