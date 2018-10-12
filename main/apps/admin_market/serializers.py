# coding:utf-8

from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Goods, GoodsCategory


class GoodsCategorySerializer(serializers.ModelSerializer):

    operator_name = serializers.CharField(
        source='operator_name.user_name',
        read_only=True
    )

    class Meta:
        model = GoodsCategory
        fields = (
            'id',
            'category_name',
            'create_time',
            'is_active',
            'update_time',
            'operator_name'
        )


class CreateGoodsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = (
            'id',
            'category_name',
            'is_active'
        )


class GoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.category_name',
        read_only=True
    )

    operator_name = serializers.CharField(
        source='operator_name.user_name',
        read_only=True
    )

    class Meta:
        model = Goods
        fields = (
            'id',
            'goods_name',
            'category_name',
            'goods_price',
            'is_active',
            'need_integral',
            'is_integral',
            'create_time',
            'update_time',
            'operator_name',
            'is_promotion',
            'is_special',
            'vip_info'
        )


class CreateGoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.category_name',
        read_only=True
    )

    def validate(self, attrs):
        is_special = attrs.get("is_special")
        vip_info = attrs.get("vip_info")

        if is_special and not vip_info:
            raise serializers.ValidationError("请选择会员权益")
        return attrs

    class Meta:
        model = Goods
        fields = (
            'id',
            'goods_name',
            'category',
            'goods_price',
            'is_active',
            'is_integral',
            'need_integral',
            'category_name',
            'is_promotion',
            'is_special',
            'vip_info'
        )
