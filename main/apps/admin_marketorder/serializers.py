# coding:utf-8
# Time    : 2018/9/26 下午9:40
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from django.db import transaction

from main.models import Order, MarketOrderDetail, OrderPay, OrderRefunded, PayType
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
            "nums",
            "consignee_name",
            "consignee_address",
            "consignee_phone",
            "order_goods_price"
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


class OrderSerializer(serializers.ModelSerializer):
    market_order_detail = MarketOrderDetailSerializer(read_only=True)
    order_refunded = OrderRefundedSerializer(read_only=True)
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
            "user_remark"
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
            "user_remark"
        )


class RefundedSerializer(serializers.ModelSerializer):

    @transaction.atomic
    def update(self, instance, validated_data):
        # 进行退款操作, 创建退款信息
        if self.instance.order_status != OrderStatus.prp_refund:
            raise serializers.ValidationError({"non_field_errors": ['当前订单状态无法操作退款']})

        if self.instance.pay_type == PayType.integral:
            # 将积分退回.并把状态更改为已退款
            params = {
                "order": instance,
                "refunded_integral": self.instance.order_pay.integral
            }
            # 用户积分增加上来
            validated_data.update({"order_status": OrderStatus.refunded})
        elif self.instance.pay_type == PayType.balance:
            # 将余额退回相应的地方。并把状态更改为已退款
            params = {
                "order": instance,
                "refunded_money": self.instance.order_pay.money,
                "refunded_free_money": self.instance.order_pay.free_money
            }
        else:
            pass

    class Meta:
        model = Order
        fields = "__all__"
