# coding:utf-8

from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Goods, GoodsCategory


class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.category_name',
        read_only=True
    )

    class Meta:
        model = Goods
        fields = (
            'id',
            'goods_name',
            'category_name',
            'goods_price',
            'is_active'
        )
