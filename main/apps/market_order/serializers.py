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
            'pay_money',
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
        consumer = self.context['request'].user.consumer
        # 这里判断用户是否为会员等
        goods = attrs.pop("goods", '')
        if not goods:
            raise serializers.ValidationError({"goods": ['goods字段商必须存在']})
        goods_name = goods.get("goods_name")
        goods = Goods.objects.filter(goods_name=goods_name).filter().first()
        if not goods:
            raise serializers.ValidationError({"goods": ['商品不存在']})
        if consumer.is_vip:
            from decimal import Decimal
            attrs.update({"sale_price": goods.goods_price * Decimal(0.8)})  # TODO 这里折扣需要重新编辑
        else:
            attrs.update({"sale_price": goods.goods_price})
        attrs.update({"goods": goods})
        return attrs

    class Meta:
        model = MarketOrderDetail
        fields = (
            'goods',
            'nums',
            'sale_price',
        )
        read_only_fields = ('sale_price', )


class CreateMarketOrderSerializer(serializers.ModelSerializer):
    market_order_detail = CreateMarketOrderDetailSerializer(many=True)

    @atomic
    def create(self, validated_data):
        market_order_detail_list = validated_data.pop('market_order_detail', None)
        # 这里需要计算出本次订单的金额以及积分
        validated_data.update({"order_status": 20})
        instance = super(CreateMarketOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        price_num = 0
        for market_order_detail in market_order_detail_list:
            price_num += market_order_detail.get('sale_price')
            market_order_detail.update({"market_order": instance})
            MarketOrderDetail.objects.create(**market_order_detail)
        instance.pay_money = price_num
        instance.save()
        return instance

    class Meta:
        model = MarketOrder
        fields = (
            'make_order_id',
            'user_remark',
            'consignee_name',
            'consignee_address',
            'consignee_phone',
            'market_order_detail',
            'pay_money'
        )
        read_only_fields = ('make_order_id', 'pay_money')
