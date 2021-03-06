# coding:utf-8
# Time    : 2018/10/20 下午10:20
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import logging
import datetime

from rest_framework import serializers
from django.db import transaction

from main import models
from main.common.defines import OrderStatus, PayType, RefundedStatus, WeiXinCode
from main.apps.wx_pay.utils import unified_refunded
from main.common import utils

logger = logging.getLogger(__name__)


class UserRefundedInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserRefundedInfo
        fields = (
            'id',
            'user_express_id',
            'user_express',
            "remark",
            'create_time'
        )


class HotelOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.HotelOrderDetail
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


class MarketOrderDetailSerializer(serializers.ModelSerializer):
    goods_name = serializers.CharField(
        source='goods.goods_name',
        read_only=True
    )

    class Meta:
        model = models.MarketOrderDetail
        fields = (
            'id',
            'goods',
            'goods_name',
            'goods_price',
            'goods_integral',
            'cover_image',
            "nums",
            'single_goods_amount'
        )


class OrderPaySerializer(serializers.ModelSerializer):
    # 订单支付信息
    class Meta:
        model = models.OrderPay
        fields = "__all__"


class OrderRefundedSerializer(serializers.ModelSerializer):
    refunded_status_display = serializers.CharField(
        source='get_refunded_status_display',
        read_only=True
    )
    order_id = serializers.CharField(
        source="order.order_id",
        read_only=True
    )

    class Meta:
        model = models.OrderRefunded
        fields = (
            "id",
            "order",
            "order_id",
            "refunded_status",
            "refunded_status_display",
            "refunded_message",
            "refunded_order_id",
            "refunded_money",
            "refunded_free_money",
            "refunded_integral",
            "create_time",
            "refunded_account"
        )


class MarketOrderContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MarketOrderContact
        fields = "__all__"


class MarketOrderExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MarketOrderExpress
        fields = (
            "id",
            "express_id",
            "express_name"
        )


class MarketRefundedAdminInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdminRefundedInfo
        fields = "__all__"


class MarketRefundedSerializer(serializers.ModelSerializer):
    refunded_money = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)
    refunded_integral = serializers.IntegerField(default=0, write_only=True)
    user_refunded_info = UserRefundedInfoSerializer(read_only=True)
    market_order_detail = MarketOrderDetailSerializer(many=True, read_only=True)
    order_refunded = OrderRefundedSerializer(read_only=True)
    market_order_contact = MarketOrderContactSerializer(read_only=True)
    order_express = MarketOrderExpressSerializer(read_only=True)
    order_pay = OrderPaySerializer(read_only=True)
    order_type_display = serializers.CharField(
        source="get_order_type_display",
        read_only=True
    )
    order_status_display = serializers.CharField(
        source="get_order_status_display",
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source="get_pay_type_display",
        read_only=True
    )
    consumer_name = serializers.CharField(
        source="consumer.user_name",
        read_only=True
    )
    operator_name_display = serializers.CharField(
        source="operator_name.user_name",
        read_only=True
    )

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

    def increase_integral(self, instance, refunded_integral):
        # 用户积分增加上来
        goods_name = self.get_goods_name(instance, 'integral')
        integral_param = {
            "consumer": instance.consumer,
            "integral": refunded_integral,
            "integral_type": 10,
            "remark": "增加,商品退款:{},商品名称:{}".format(refunded_integral, goods_name)
        }
        models.IntegralDetail.objects.create(**integral_param)
        instance.consumer.integral_info.integral += refunded_integral
        instance.consumer.integral_info.save()

    def increase_balance(self, instance, refunded_money):
        # 首先退免费余额
        order_pay = instance.order_pay
        consumer = instance.consumer

        free_money = refunded_money - order_pay.free_money
        re_recharge_money = 0
        if free_money > 0:
            # 表示还要退会充值余额
            re_free_money = order_pay.free_money
            re_recharge_money = free_money
            recharge_money = free_money
            consumer.free_balance = consumer.free_balance + order_pay.free_money
            consumer.recharge_balance = consumer.recharge_balance + recharge_money

        else:
            re_free_money = refunded_money
            # 表示不用退充值余额。
            consumer.free_balance = consumer.free_balance + refunded_money
            # 生成余额详情
        consumer.save()
        # 退换余额
        goods_name = self.get_goods_name(instance, 'money')
        # 用户余额明细
        balance_info = {
            "consumer": consumer,
            "balance_type": 10,
            "message": "增加,商品退款:{},商品名称:{}".format(instance.order_amount, goods_name),
            "cost_price": refunded_money,
            "left_balance": instance.consumer.balance + instance.order_amount
        }
        models.ConsumerBalance.objects.create(**balance_info)

        return re_recharge_money, re_free_money

    def validate(self, attrs):
        refunded_money = attrs.get("refunded_money")
        refunded_integral = attrs.get("refunded_integral")

        if not any((refunded_integral, refunded_money)):
            raise serializers.ValidationError("退款金额与退款积分必须存在一个")

        if refunded_money and refunded_money < 0:
            raise serializers.ValidationError("退款金额不能够为负")

        if refunded_integral and refunded_integral < 0:
            raise serializers.ValidationError("退款积分不能够为负")
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        # 进行退款操作, 创建退款信息
        refunded_money = validated_data.pop("refunded_money", 0)
        refunded_integral = validated_data.pop("refunded_integral", 0)
        if self.instance.order_status != OrderStatus.pre_refund:
            raise serializers.ValidationError({"non_field_errors": ['当前订单状态无法操作退款']})

        if refunded_money > instance.order_amount:
            raise serializers.ValidationError({"non_field_errors": ["退款金额不能够超过订单总额"]})

        if refunded_integral > instance.integral:
            raise serializers.ValidationError({"non_field_errors": ["退款积分不能够超过订单总额"]})

        # 根据订单类型来退款。。如果是商场订单。每个都要去扣除
        if self.instance.pay_type == PayType.balance:
            # 将余额退回相应的地方。并把状态更改为已退款
            if self.instance.integral:
                self.increase_integral(instance, refunded_integral)
            money, free_money = self.increase_balance(instance, refunded_money)
            params = {
                "order": instance,
                "refunded_money": money,
                "refunded_free_money": free_money,
                "refunded_account": datetime.datetime.now(),
                "refunded_integral": refunded_integral,
                "refunded_status": RefundedStatus.success
            }

            validated_data.update({"order_status": OrderStatus.refunded})
        else:
            params = {
                "order": instance,
                "refunded_money": refunded_money,
                "refunded_integral": refunded_integral
            }
            validated_data.update({"order_status": OrderStatus.refund_ing})
        order_refunded = models.OrderRefunded.objects.create(**params)
        order_refunded.refunded_order_id = order_refunded.make_order_id()
        order_refunded.save()

        consumer = instance.consumer
        if instance.pay_type == PayType.weixin:
            order_pay = models.OrderPay.objects.filter(order=instance).first()
            result = unified_refunded(order_pay.wx_order_id,
                                      order_refunded.refunded_order_id,
                                      instance.order_amount,
                                      refunded_money,
                                      consumer.openid)
            if result.get("return_code") == WeiXinCode.success and result.get("result_code") == WeiXinCode.success:
                order_refunded.refunded_status = RefundedStatus.success
                order_refunded.refunded_message = "退款成功"
                order_refunded.refunded_account = datetime.datetime.now()
                validated_data.update({"order_status": OrderStatus.refunded})
            elif result.get("return_code") == WeiXinCode.success and result.get("err_code"):
                order_refunded.refunded_status = RefundedStatus.fail
                order_refunded.refunded_message = result.get("err_code_des") or ''
            else:
                order_refunded.refunded_status = RefundedStatus.retry
                order_refunded.refunded_message = result.get("return_msg") or ''

            order_refunded.save()

        instance = super(MarketRefundedSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = models.Order
        fields = (
            "id",
            "market_order_detail",
            "order_refunded",
            "market_order_contact",
            "order_express",
            "order_pay",
            "order_type",
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark",
            "operator_remark",
            "operator_name_display",
            'refunded_integral',
            'refunded_money',
            'user_refunded_info',
            'refund_reason'
        )
        read_only_fields = (
            "order_type",
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark",
            'refund_reason'
        )


class MarketRefundedApplySerializer(serializers.ModelSerializer):
    # 同意或者拒绝退款申请
    admin_refunded_info = MarketRefundedAdminInfoSerializer()

    def validate(self, attrs):
        order_status = attrs.get("order_status")
        admin_refunded_info = attrs.get("admin_refunded_info") or {}
        if not order_status:
            raise serializers.ValidationError("请传递订单状态")

        if order_status == OrderStatus.fill_apply:
            if not admin_refunded_info:
                raise serializers.ValidationError("请传递退款邮寄信息")
            for k, v in admin_refunded_info.items():
                if k in ('refunded_address', 'refunded_name', 'refunded_phone') and not v:
                    raise serializers.ValidationError("请传递退款邮寄信息")

        if order_status == OrderStatus.refunded_fail:
            fail_reason = attrs.get("fail_reason") or ''
            if not fail_reason:
                raise serializers.ValidationError("退款拒绝请传递原因")

        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        admin_refunded_info = validated_data.pop("admin_refunded_info")

        if instance.order_status != OrderStatus.apply_refund:
            raise serializers.ValidationError({"non_field_errors": ['当前订单无法操作']})
        instance = super(MarketRefundedApplySerializer, self).update(instance, validated_data)
        if admin_refunded_info:
            admin_refunded_info.update({"order": instance})
            models.AdminRefundedInfo.objects.create(**admin_refunded_info)

        return instance

    class Meta:
        model = models.Order
        fields = (
            "id",
            "order_status",
            "admin_refunded_info",
            'fail_reason'
        )


class HotelOrderApplySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        order_status = attrs.get("order_status")
        fail_reason = attrs.get("fail_reason")
        if order_status == OrderStatus.refunded_fail:
            if not fail_reason:
                raise serializers.ValidationError("拒绝退款时,请传递退款拒绝原因")
        return attrs

    def update(self, instance, validated_data):
        if validated_data['order_status'] == OrderStatus.pre_refund:
            utils.increase_room_num(instance)
        instance = super(HotelOrderApplySerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = models.Order
        fields = (
            'id',
            "order_status",
            "fail_reason"
        )


class HotelOrderRefundedSerializer(serializers.ModelSerializer):

    refunded_money = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=True)
    order_refunded = OrderRefundedSerializer(read_only=True)
    order_pay = OrderPaySerializer(read_only=True)

    pay_type_display = serializers.CharField(
        source="get_pay_type_display",
        read_only=True
    )
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    order_type_display = serializers.CharField(
        source='get_order_type_display',
        read_only=True
    )
    consumer_name = serializers.CharField(
        source="consumer.user_name",
        read_only=True
    )
    operator_name_display = serializers.CharField(
        source="operator_name.user_name",
        read_only=True
    )
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )

    def validate(self, attrs):
        if self.instance.order_status != OrderStatus.pre_refund:
            raise serializers.ValidationError("当前订单不可退款")
        refunded_money = attrs.get("refunded_money")
        if not refunded_money:
            raise serializers.ValidationError("请传递退款金额")

        if self.instance.order_amount < refunded_money:
            raise serializers.ValidationError("退款金额不能够超过订单总额")

        if refunded_money < 0:
            raise serializers.ValidationError("退款金额不能改为负")

        return attrs

    @staticmethod
    def increase_balance(instance, refunded_money):
        order_pay = instance.order_pay
        consumer = instance.consumer
        # 首先退免费余额
        free_money = refunded_money - order_pay.free_money
        re_recharge_money = 0
        if free_money > 0:
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
        models.ConsumerBalance.objects.create(**balance_detail)

        refunded_info = {
            "order": instance,
            "refunded_money": re_recharge_money,
            "refunded_free_money": re_free_money,
            "refunded_account": datetime.datetime.now(),
            "refunded_status": RefundedStatus.success
        }
        return refunded_info

    @transaction.atomic
    def update(self, instance, validated_data):
        # 住宿退款。
        validated_data.update({"operator_time": datetime.datetime.now()})
        consumer = instance.consumer
        # 如果支付类型为余额支付。返回给余额
        pay_type = instance.pay_type
        refunded_money = validated_data.pop('refunded_money')
        if pay_type == PayType.balance:
            validated_data.update({"order_status": OrderStatus.refunded})
            refunded_info = self.increase_balance(instance, refunded_money)
        else:
            # 创建退款信息
            refunded_info = {
                "order": instance,
                "refunded_money": refunded_money,
                "refunded_status": RefundedStatus.refunded_ing
            }
            validated_data.update({"order_status": OrderStatus.refund_ing})

        order_refunded = models.OrderRefunded.objects.create(**refunded_info)
        order_refunded.refunded_order_id = order_refunded.make_order_id()
        order_refunded.save()

        if instance.pay_type == PayType.weixin:
            order_pay = models.OrderPay.objects.filter(order=instance).first()
            result = unified_refunded(order_pay.wx_order_id,
                                      order_refunded.refunded_order_id,
                                      instance.order_amount,
                                      order_refunded.refunded_money,
                                      consumer.openid)
            logger.info("order_id:{},refunded:{}".format(instance.order_id, result))
            if result.get("return_code") == WeiXinCode.success and result.get("result_code") == WeiXinCode.success:
                order_refunded.refunded_status = RefundedStatus.success
                order_refunded.refunded_message = "退款成功"
                order_refunded.refunded_account = datetime.datetime.now()
                validated_data.update({"order_status": OrderStatus.refunded})
            elif result.get("return_code") == WeiXinCode.success and result.get("err_code"):
                order_refunded.refunded_status = RefundedStatus.fail
                order_refunded.refunded_message = result.get("err_code_des") or ''
            else:
                order_refunded.refunded_status = RefundedStatus.retry
                order_refunded.refunded_message = result.get("err_code_des") or ''

            order_refunded.save()

            logger.info("refunded result:{}".format(result))
        instance = super(HotelOrderRefundedSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = models.Order
        fields = (
            "id",
            "order_refunded",
            'belong_hotel_name',
            'belong_hotel',
            "order_pay",
            "order_type",
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark",
            "operator_remark",
            "refunded_money",
            "operator_name_display",
            'refund_reason'
        )
        read_only_fields = (
            "order_type",
            'belong_hotel',
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark",
            'refund_reason'
        )


class MarketOrderRetryRefundedSerializer(serializers.ModelSerializer):
    market_order_detail = MarketOrderDetailSerializer(many=True, read_only=True)
    order_refunded = OrderRefundedSerializer(read_only=True)
    market_order_contact = MarketOrderContactSerializer(read_only=True)
    order_express = MarketOrderExpressSerializer(read_only=True)
    order_pay = OrderPaySerializer(read_only=True)
    order_type_display = serializers.CharField(
        source="get_order_type_display",
        read_only=True
    )
    order_status_display = serializers.CharField(
        source="get_order_status_display",
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source="get_pay_type_display",
        read_only=True
    )
    consumer_name = serializers.CharField(
        source="consumer.user_name",
        read_only=True
    )
    operator_name_display = serializers.CharField(
        source="operator_name.user_name",
        read_only=True
    )

    def validate(self, attrs):
        # 这里需要判断订单退款状态是否是在退款中并且退款信息为失败或者重试
        if self.instance.order_status != OrderStatus.refund_ing and self.instance.order_refunded.refunded_status not in (RefundedStatus.retry, RefundedStatus.fail):
            raise serializers.ValidationError("重复支付错误, 订单状态有误")
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        # 根据退款信息重新支付.只有微信支付的会出现问题
        if instance.pay_type != PayType.weixin:
            raise serializers.ValidationError({"non_field_error":['当前订单不支持重试']})
        validated_data.update({"operator_time": datetime.datetime.now()})
        order_refunded = self.instance.order_refunded
        consumer = instance.consumer
        order_pay = models.OrderPay.objects.filter(order=instance).first()
        result = unified_refunded(order_pay.wx_order_id,
                                  order_refunded.refunded_order_id,
                                  instance.order_amount,
                                  order_refunded.refunded_money,
                                  consumer.openid)
        logger.warning("retry order_id:{}, result:{}".format(instance.order_id, result))
        if result.get("return_code") == WeiXinCode.success and result.get("result_code") == WeiXinCode.success:
            order_refunded.refunded_status = RefundedStatus.success
            order_refunded.refunded_message = "退款成功"
            order_refunded.refunded_account = datetime.datetime.now()
            validated_data.update({"order_status": OrderStatus.refunded})
        elif result.get("return_code") == WeiXinCode.success and result.get("err_code"):
            order_refunded.refunded_status = RefundedStatus.fail
            order_refunded.refunded_message = result.get("err_code_des") or ''
        else:
            order_refunded.refunded_status = RefundedStatus.retry
            order_refunded.refunded_message = result.get("err_code_des") or ''

        order_refunded.save()
        logger.info("refunded result:{}".format(result))
        instance = super(MarketOrderRetryRefundedSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = models.Order
        fields = (
            "id",
            "market_order_detail",
            "order_refunded",
            "market_order_contact",
            "order_express",
            "order_pay",
            "order_type",
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark",
            "operator_remark",
            "operator_name_display"
        )
        read_only_fields = (
            "order_type",
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark"
        )


class HotelOrderRetryRefundedSerializer(serializers.ModelSerializer):

    order_refunded = OrderRefundedSerializer(read_only=True)
    order_pay = OrderPaySerializer(read_only=True)

    pay_type_display = serializers.CharField(
        source="get_pay_type_display",
        read_only=True
    )
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    order_type_display = serializers.CharField(
        source='get_order_type_display',
        read_only=True
    )
    consumer_name = serializers.CharField(
        source="consumer.user_name",
        read_only=True
    )
    operator_name_display = serializers.CharField(
        source="operator_name.user_name",
        read_only=True
    )
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )

    def validate(self, attrs):
        # 这里需要判断订单退款状态是否是在退款中并且退款信息为失败或者重试
        if self.instance.order_status != OrderStatus.refund_ing and self.instance.order_refunded.refunded_status not in (
        RefundedStatus.retry, RefundedStatus.fail):
            raise serializers.ValidationError("重复支付错误, 订单状态有误")

        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        # 根据退款信息重新支付.只有微信支付的会出现问题
        validated_data.update({"operator_time": datetime.datetime.now()})
        order_refunded = self.instance.order_refunded
        consumer = instance.consumer
        order_pay = models.OrderPay.objects.filter(order=instance).first()
        result = unified_refunded(order_pay.wx_order_id,
                                  order_refunded.refunded_order_id,
                                  instance.order_amount,
                                  order_refunded.refunded_money,
                                  consumer.openid)
        if result.get("return_code") == WeiXinCode.success and result.get("result_code") == WeiXinCode.success:
            order_refunded.refunded_status = RefundedStatus.success
            order_refunded.refunded_message = "退款成功"
            order_refunded.refunded_account = datetime.datetime.now()
            validated_data.update({"order_status": OrderStatus.refunded})
        elif result.get("return_code") == WeiXinCode.success and result.get("err_code"):
            order_refunded.refunded_status = RefundedStatus.fail
            order_refunded.refunded_message = result.get("err_code_des") or ''
        else:
            order_refunded.refunded_status = RefundedStatus.retry
            order_refunded.refunded_message = result.get("return_msg") or ''

        order_refunded.save()
        logger.info("refunded result:{}".format(result))
        instance = super(HotelOrderRetryRefundedSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = models.Order
        fields = (
            "id",
            "order_refunded",
            "belong_hotel",
            "belong_hotel_name",
            "order_pay",
            "order_type",
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark",
            "operator_remark",
            "operator_name_display"
        )
        read_only_fields = (
            "order_type",
            "order_type_display",
            "order_id",
            "order_status",
            "order_status_display",
            "create_time",
            "pay_time",
            "pay_type",
            "pay_type_display",
            "num",
            "order_amount",
            "integral",
            "consumer",
            "consumer_name",
            "operator_name",
            "operator_time",
            "user_remark",
            'belong_hotel'
        )