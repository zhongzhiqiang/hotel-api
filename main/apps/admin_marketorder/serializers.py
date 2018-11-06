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

from main.models import (Order, MarketOrderDetail, OrderPay, OrderRefunded, PayType, IntegralDetail,
                         ConsumerBalance, MarketOrderContact, MarketOrderExpress)
from main.common.defines import OrderStatus


class MarketOrderDetailSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(
        source='goods.goods_name',
        read_only=True
    )
    is_integral = serializers.BooleanField(
        source='goods.is_integral',
        read_only=True
    )

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'goods_name',
            'goods_price',
            'goods_integral',
            'cover_image',
            "nums",
            'is_integral',
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


class MarketOrderExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrderExpress
        fields = (
            "id",
            "express_id",
            "express_name"
        )


class OrderSerializer(serializers.ModelSerializer):
    market_order_detail = MarketOrderDetailSerializer(many=True, read_only=True)
    order_refunded = OrderRefundedSerializer(read_only=True)
    market_order_contact = MarketOrderContactSerializer(read_only=True)
    order_express = MarketOrderExpressSerializer()

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

    def validate(self, attrs):
        order_status = attrs.get("order_status")
        order_express = attrs.get("order_express")
        # 当后端传递待收货
        if order_status and order_status == OrderStatus.take_deliver:
            if not order_express:
                raise serializers.ValidationError("请传递信息")
        return attrs

    def update(self, instance, validated_data):
        validated_data.update({"operator_time": datetime.datetime.now()})
        instance = super(OrderSerializer, self).update(instance, validated_data)
        return instance

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
            'market_order_contact',
            'order_express'
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
            'market_order_contact',
            'market_order_detail',
            'order_refunded'
        )