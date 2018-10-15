# coding:utf-8
# Time    : 2018/8/23 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import logging
import datetime

from rest_framework import serializers
from django.db import transaction

from main.models import Order, HotelOrderDetail, OrderPay, OrderRefunded, ConsumerBalance
from main.apps.admin_integral.utils import get_integral, make_integral
from main.common.defines import OrderStatus, PayType

logger = logging.getLogger(__name__)


class HotelOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style',
            'room_nums',
            'room_price',
            "reserve_check_in_time",
            "reserve_check_out_time",
            "contact_name",
            "contact_phone",
            "room_style_name",
            "days"
        )


class OrderPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPay
        fields = (
            "id",
            "wx_order_id",
            "free_money",
            "integral",
            "money",
            "create_time"
        )


class HotelOrderInfoSerializer(serializers.ModelSerializer):
    hotel_order_detail = HotelOrderDetailSerializer(read_only=True)
    order_pay = OrderPaySerializer(read_only=True)

    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True
    )

    @staticmethod
    def make_integral(instance):
        integral = get_integral(instance.sale_price)
        remark = "住宿:%s,积分:%s" % (instance.hotelorderdetail.room_style.style_name, integral)
        make_integral(instance.consumer, integral, remark)

    def validate(self, attrs):
        order_status = attrs.get("order_status")
        if order_status and order_status < self.instance.order_status:
            raise serializers.ValidationError("当前订单状态为:{}".format(self.instance.get_order_status_display()))
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        order_status = validated_data.get("order_status")

        # 生成积分是，当用户入住完成时
        if order_status == OrderStatus.success and instance.order_status == OrderStatus.check_in:
            try:
                self.make_integral(instance)
            except Exception as e:
                logger.warning("make integral error:{}".format(e), exc_info=True)
                raise serializers.ValidationError("生成积分失败")
            validated_data.update({"order_status": OrderStatus.success})
        instance = super(HotelOrderInfoSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = Order
        fields = (
            "id",
            'hotel_order_detail',
            'order_pay',
            "order_id",
            "belong_hotel",
            "belong_hotel_name",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_type",
            "pay_type_display",
            "pay_time",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "operator_name",
            "operator_time",
            "refund_reason",
            "user_remark",
            "operator_remark"
        )
        read_only_fields = (
            "order_id",
            "belong_hotel",
            "pay_type",
            "pay_time",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "operator_name",
            "operator_time",
            "refund_reason",
            "user_remark"
        )


class HotelOrderRefundedSerializer(serializers.ModelSerializer):

    refunded_money = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=True)


    @transaction.atomic
    def update(self, instance, validated_data):
        # 住宿退款。
        consumer = instance.consumer
        # 如果支付类型为余额支付。返回给余额
        pay_type = instance.pay_type
        refunded_money = validated_data.pop('refunded_money')
        if pay_type == PayType.balance:
            order_pay = instance.order_pay

            # 首先退免费余额
            free_money = refunded_money - order_pay.free_money
            re_recharge_money = 0
            if refunded_money > 0:
                # 表示还要退会充值余额
                re_free_money = order_pay.free_money
                re_recharge_money = free_money

                recharge_money = free_money
                consumer.free_balance = consumer.free_balance + order_pay.free_money
                consumer.recharge_balance = consumer.recharge_balance + recharge_money
                consumer.save()
            else:
                re_free_money = refunded_money
                # 表示不用退充值余额。
                consumer.free_balance = consumer.free_balance + refunded_money
                consumer.save()
                # 生成余额详情
            balance_detail = {
                "consumer": consumer,
                "balance_type": 10,
                "message": "退款, 住宿订单退款:{}".format(refunded_money),
                "cost_price": refunded_money,
                "left_balance": consumer.balance
            }
            ConsumerBalance.objects.create(**balance_detail)
            refunded_info = {
                "order": instance,
                "refunded_money": re_recharge_money,
                "refunded_free_money": re_free_money,
                "refunded_account": datetime.datetime.now()
            }
            validated_data.update({"order_status": OrderStatus.refunded})
        else:
            # 创建退款信息
            refunded_info = {
                "order": instance,
                "refunded_money": refunded_money,
            }
            validated_data.update({"order_status": OrderStatus.refund_ing})

        order_refunded = OrderRefunded(**refunded_info)
        order_refunded.save()
        order_refunded.refunded_order_id = order_refunded.make_order_id()
        order_refunded.save()
        instance = super(HotelOrderRefundedSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = Order
        fields = (
            'id',
            'refunded_money'
        )
