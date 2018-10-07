# coding:utf-8
# Time    : 2018/9/8 下午8:27
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime

from django.db.transaction import atomic
from rest_framework import serializers

from main.models import MarketOrder, MarketOrderDetail, ConsumerBalance
from main.common.defines import PayType, MarketOrderStatus


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
            'id',
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
        read_only_fields = ('order_id', 'create_time', 'order_status',
                            'pay_time', 'goods_count', 'pay_money')


class CreateMarketOrderDetailSerializer(serializers.ModelSerializer):

    goods_name = serializers.CharField(
        source='goods.goods_name',
        read_only=True
    )

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
            'goods_name',
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
        # 步骤1。判断支付类型，
        # 步骤2。积分兑换。
        # 步骤3。余额兑换
        # 步骤4。微信支付
        consumer = self.context['request'].user.consumer

        if validated_data['pay_type'] == PayType.integral:
            left_integral = consumer.integral - validated_data['pay_integral']
            validated_data.update({"order_status": MarketOrderStatus.wait_deliver})
            validated_data.update({"pay_time": datetime.datetime.now()})
            consumer.integral = left_integral
            consumer.save()
        elif validated_data['pay_type'] == PayType.balance:
            validated_data.update({"order_status": MarketOrderStatus.wait_deliver})
            validated_data.update({"pay_time": datetime.datetime.now()})

            left_balance = consumer.recharge_balance - validated_data['pay_money']
            if left_balance < 0:
                left_balance = consumer.free_balance - left_balance
                consumer.recharge_balance = 0
                consumer.free_balance = left_balance
            else:
                consumer.recharge_balance = left_balance
            consumer.save()
            params = {
                "consumer": consumer,
                "balance_type": 20,
                "message": "余额消费,购买商品:{},数量:{}".format(
                    market_order_detail['goods'].goods_name, market_order_detail['nums']),
                "cost_price": -validated_data['pay_money'],
                "left_balance": consumer.balance,
            }
            ConsumerBalance(**params).save()
        else:
            validated_data.update({"order_status": MarketOrderStatus.unpay})
            
        instance = super(CreateMarketOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        market_order_detail.update({"market_order": instance})
        MarketOrderDetail.objects.create(**market_order_detail)
        return instance

    class Meta:
        model = MarketOrder
        fields = (
            'order_id',
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
