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
from main.common.defines import PayType


class MarketOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'sale_price',
            'nums',
        )


class MarketOrderSerializer(serializers.ModelSerializer):
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    marketorderdetail = MarketOrderDetailSerializer()

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
            'marketorderdetail',
            'consignee_name',
            'consignee_address',
            'consignee_phone',
        )


class CreateMarketOrderDetailSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        goods = attrs.get("goods")
        if not goods:
            raise serializers.ValidationError("商品不存在")

        return attrs

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'nums',
            'sale_price',
            'integral')
        read_only_fields = ('sale_price', 'integral')


class CreateMarketOrderSerializer(serializers.ModelSerializer):
    marketorderdetail = CreateMarketOrderDetailSerializer()

    def validate(self, attrs):
        consumer = self.context['request'].user.consumer
        order_detail = attrs['marketorderdetail']
        goods = order_detail['goods']

        pay_type = attrs.get("pay_type") or PayType.weixin
        if pay_type == PayType.integral and not goods.is_integral:
            raise serializers.ValidationError("当前商品不支持积分兑换")

        unit_integral = 0  # 积分单价
        need_price = 0  # 当前用户需要支付金额
        need_integral = 0  # 当前用户需要花费金额
        unit_price = 0
        if pay_type == PayType.integral:
            unit_integral = goods.need_integral
            need_integral = unit_integral * order_detail['nums']
            if need_integral > consumer.integral:
                raise serializers.ValidationError("积分不足, 无法兑换")
        elif pay_type == PayType.balance:
            unit_price = goods.goods_price
            need_price = unit_price * order_detail['nums']
            if need_price > consumer.balance:
                raise serializers.ValidationError("用户余额不足, 无法购买")
        else:
            unit_price = goods.goods_price
            need_price = unit_price * order_detail['nums']
        attrs.update({"pay_integral": need_integral, "pay_money": need_price})
        order_detail.update({"sale_price": unit_price, "integral": unit_integral})
        return attrs

    @atomic
    def create(self, validated_data):
        market_order_detail = validated_data.pop('marketorderdetail', None)

        # 这里需要计算出本次订单的金额以及积分
        validated_data.update({"order_status": 20})
        instance = super(CreateMarketOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        market_order_detail.update({"market_order": instance})
        MarketOrderDetail.objects.create(**market_order_detail)
        # 这里进行余额减。以及积分剪除并有余额详情
        return instance

    class Meta:
        model = MarketOrder
        fields = (
            'make_order_id',
            'user_remark',
            'consignee_name',
            'consignee_address',
            'consignee_phone',
            'marketorderdetail',
            'pay_money',
            'pay_type',
            'pay_integral',
        )
        read_only_fields = ('make_order_id', 'pay_money', 'pay_integral')
