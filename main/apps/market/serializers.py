# coding:utf-8

from rest_framework import serializers

from main.models import GoodsCategory, Goods


class GoodsSerializer(serializers.ModelSerializer):
    goods_category = serializers.CharField(
        source='category.category_name',
        read_only=True
    )

    class Meta:
        model = Goods
        fields = (
            'id',
            "goods_name",
            'goods_price',
            'goods_category'
        )


class GoodsCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = (
            'id',
            'category_name',
        )
