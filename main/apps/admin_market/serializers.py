# coding:utf-8

from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from main.models import Goods, GoodsCategory, VipSettings


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


class VIPInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VipSettings
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.category_name',
        read_only=True
    )

    operator_name = serializers.CharField(
        source='operator_name.user_name',
        read_only=True
    )
    vip_info = VIPInfoSerializer(read_only=True)
    images = serializers.ListField(child=serializers.CharField())

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
            'vip_info',
            'images',
            'cover_image'
        )


class CreateGoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.category_name',
        read_only=True
    )

    images = serializers.ListField(child=serializers.CharField())

    def validate(self, attrs):
        is_special = attrs.get("is_special")
        vip_info = attrs.get("vip_info")

        if is_special and not vip_info:
            raise serializers.ValidationError("请选择会员权益")

        is_integral = attrs.get("is_integral")
        need_integral = attrs.get("need_integral")
        goods_price = attrs.get("goods_price")

        if is_integral and not need_integral:
            raise serializers.ValidationError("请传递需要兑换积分")

        if not is_integral and not goods_price:
            raise serializers.ValidationError("请传递商品单价")

        distribution_method = attrs.get("distribution_method")
        distribution_bonus = attrs.get("distribution_bonus") or 0
        distribution_ratio = attrs.get("distribution_ratio")

        if distribution_method == 'fixed':
            if not distribution_bonus:
                raise serializers.ValidationError("请传递固定分销金额")

        elif distribution_method == 'ratio':
            if distribution_ratio > 1.0 or distribution_ratio < 0:
                raise serializers.ValidationError("请传递正确的分销比例.[0-1.0]之间")

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
            'vip_info',
            'cover_image',
            'images',
            'distribution_method',
            'distribution_bonus',
            'distribution_ratio'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Goods.objects.all(),
                fields=('is_integral', 'goods_name'),
                message='已有商品相同配置'
            )
        ]
