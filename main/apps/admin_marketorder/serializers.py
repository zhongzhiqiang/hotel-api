# coding:utf-8
# Time    : 2018/9/26 下午9:40
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import MarketOrderDetail, MarketOrder


class MarketOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrderDetail
        fields = "__all__"


class MarketOrderSerializer(serializers.ModelSerializer):
    marketorderdetail = MarketOrderDetailSerializer(read_only=True)

    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True
    )
    consumer = serializers.CharField(
        source='consumer.user_name',
        allow_blank=True,
        read_only=True
    )

    class Meta:
        model = MarketOrder
        fields = (
            'id',
            'marketorderdetail',
            'order_id',
            'order_status',
            'order_status_display',
            'create_time',
            'pay_type',
            'pay_type_display',
            'pay_money',
            'pay_integral',
            'pay_time',
            'operator_time',
            'user_remark',
            'operator_remark',
            'consumer',
            'consignee_name',
            'consignee_address',
            'consignee_phone'
        )
        read_only_fields = ("order_id", "pay_type", 'pay_money', 'pay_integral',
                            'pay_time', 'operator_time', 'user_remark',
                            'consumer', 'consignee_name', 'consignee_address',
                            'consignee_phone')
