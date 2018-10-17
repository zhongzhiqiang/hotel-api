# coding:utf-8
# Time    : 2018/9/26 下午9:40
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime

from rest_framework import serializers
from django.db import transaction

from main.models import Order, MarketOrderDetail, OrderPay, OrderRefunded, PayType, IntegralDetail, ConsumerBalance, MarketOrderContact
from main.common.defines import OrderStatus


class MarketOrderDetailSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(
        source='goods.name',
        read_only=True
    )

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'goods_name',
            'sale_price',
            'integral',
            'image',
            "nums",
            'single_goods_amount'
        )


class OrderPaySerializer(serializers.ModelSerializer):
    # 订单支付信息
    class Meta:
        model = OrderPay
        fields = "__all__"


class OrderRefundedSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRefunded
        fields = "__all__"


class MarketOrderContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrderContact
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    market_order_detail = MarketOrderDetailSerializer(many=True)
    order_refunded = OrderRefundedSerializer(read_only=True)
    market_order_contact = MarketOrderContactSerializer()

    order_pay = OrderPaySerializer(read_only=True)
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True
    )
    consumer_name = serializers.CharField(
        source='consumer.user_name',
        allow_blank=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'order_id',
            'order_pay',
            'market_order_detail',
            "order_refunded",
            "order_status",
            "order_status_display",
            "pay_type",
            "pay_type_display",
            "create_time",
            "pay_time",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "operator_remark",
            "refund_reason",
            "user_remark",
            'market_order_contact'
        )
        read_only_fields = (
            "pay_type",
            "order_id",
            "pay_time",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "refund_reason",
            "user_remark",
            'market_order_contact'
        )


class RefundedSerializer(serializers.ModelSerializer):

    @staticmethod
    def get_goods_name(instance, goods_type):
        goods_name = ''
        if goods_type == 'integral':
            for mark_order in instance.market_order_detail.all():
                if mark_order.is_integral:
                    if goods_name:
                        goods_name = goods_name + ',' + mark_order.goods_name

                    else:
                        goods_name = mark_order.goods_name
        else:
            for mark_order in instance.market_order_detail.all():
                if not mark_order.is_integral:
                    if goods_name:
                        goods_name = goods_name + ',' + mark_order.goods_name

                    else:
                        goods_name = mark_order.goods_name
        return goods_name

    def increase_integral(self, instance):
        # 用户积分增加上来
        goods_name = self.get_goods_name(instance, 'integral')
        integral_param = {
            "consumer": instance.consumer,
            "integral": instance.integral,
            "integral_type": 10,
            "remark": "增加,商品退款:{},商品名称:{}".format(instance.integral, goods_name)
        }
        IntegralDetail.objects.create(**integral_param)
        instance.consumer.integral_info.integral += instance.integral
        instance.consumer.integral_info.save()

    def increase_balance(self, instance):
        # 退换余额
        goods_name = self.get_goods_name(instance, 'money')
        # 用户余额明细
        balance_info = {
            "consumer": instance.consumer,
            "balance_type": 10,
            "message": "增加,商品退款:{},商品名称:{}".format(instance.order_amount, goods_name),
            "cost_price": instance.order_amount,
            "left_balance": instance.consumer.balance + instance.order_amount
        }
        ConsumerBalance.objects.create(**balance_info)
        # 退回余额。
        instance.consumer.recharge_balance = instance.consumer.recharge_balance + instance.order_pay.money
        instance.consumer.free_balance = instance.consumer.free_balance + instance.order_pay.free_money
        instance.consumer.save()

    @transaction.atomic
    def update(self, instance, validated_data):
        # 进行退款操作, 创建退款信息

        if self.instance.order_status != OrderStatus.prp_refund:
            raise serializers.ValidationError({"non_field_errors": ['当前订单状态无法操作退款']})

        # 根据订单类型来退款。。如果是商场订单。每个都要去扣除
        if self.instance.pay_type == PayType.balance:
            # 将余额退回相应的地方。并把状态更改为已退款
            params = {
                "order": instance,
                "refunded_money": self.instance.order_pay.money,
                "refunded_free_money": self.instance.order_pay.free_money,
                "refunded_account": datetime.datetime.now(),
                "refunded_integral": self.instance.integral,
            }
            if self.instance.integral:
                self.increase_integral(instance)
            self.increase_balance(instance)

            validated_data.update({"order_status": OrderStatus.refunded})
        else:
            params = {
                "order": instance,
                "refunded_money": instance.order_amount
            }
        order_refunded = OrderRefunded.objects.create(**params)
        order_refunded.refunded_order_id = order_refunded.make_order_id()
        order_refunded.save()
        instance = super(RefundedSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = Order
        fields = ("id", 'operator_remark')
