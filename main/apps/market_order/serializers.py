# coding:utf-8
# Time    : 2018/9/8 下午8:27
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db.transaction import atomic
from rest_framework import serializers

from main.models import MarketOrder, MarketOrderDetail, Goods


class MarketOrderDetailSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(
        source='goods.goods_name',
    )
    goods_category = serializers.CharField(
        source='goods.category.category_name',
        read_only=True
    )

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'goods_name',
            'goods_category',
            'sale_price',
            'nums',
        )


class MarketOrderSerializer(serializers.ModelSerializer):
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )

    market_order_detail = MarketOrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = MarketOrder
        fields = (
            'order_id',
            'order_status',
            'order_status_display',
            'create_time',
            'pay_time',
            'user_remark',
            'goods_count',
            'market_order_detail',
            'consignee_name',
            'consignee_address',
            'consignee_phone',
        )


class CreateMarketOrderDetailSerializer(serializers.ModelSerializer):

    goods = serializers.CharField(
        source='goods.goods_name'
    )

    def validate(self, attrs):
        goods = attrs.pop("goods", '')
        if not goods:
            raise serializers.ValidationError({"goods": ['goods字段商必须存在']})
        goods_name = goods.get("goods_name")
        goods = Goods.objects.filter(goods_name=goods_name).filter().first()
        if not goods:
            raise serializers.ValidationError({"goods": ['商品不存在']})
        attrs.update({"goods": goods})
        return attrs

    class Meta:
        model = MarketOrderDetail
        fields = (
            'market_order',
            'goods',
            'sale_price',
            'nums',
        )


class CreateMarketOrderSerializer(serializers.ModelSerializer):
    market_order_detail = CreateMarketOrderDetailSerializer(many=True)

    @atomic
    def create(self, validated_data):
        market_order_detail_list = validated_data.pop('market_order_detail', None)
        validated_data.update({"order_status": 20})
        instance = super(CreateMarketOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        for market_order_detail in market_order_detail_list:
            market_order_detail.update({"market_order": instance})
            MarketOrderDetail.objects.create(**market_order_detail)
        return instance

    class Meta:
        model = MarketOrder
        fields = (
            'user_remark',
            'consignee_name',
            'consignee_address',
            'consignee_phone',
            'market_order_detail'
        )
