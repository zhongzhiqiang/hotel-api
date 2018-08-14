# coding:utf-8

from rest_framework import serializers

from main.models import GoodsCategory, Goods


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = (
            'id',
            "goods_name",
            'goods_price'
        )


class GoodsCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = (
            'id',
            'category_name',
        )
