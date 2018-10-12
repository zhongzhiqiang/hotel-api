# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import logging
import datetime

from rest_framework import serializers
from django.db.transaction import atomic

from main.models import Order, HotelOrderDetail, ConsumerBalance, OrderType, MarketOrderDetail, VipMember, OrderPay, IntegralDetail
from main.common.defines import PayType, OrderStatus
from main.common.utils import create_integral_info

logger = logging.getLogger('django')


class CreateHotelOrderDetailSerializer(serializers.ModelSerializer):
    room_style_name = serializers.CharField(
        source='room_style.style_name',
        read_only=True,
    )

    def validate(self, attrs):
        room_style = attrs.get("room_style")
        if not room_style:
            raise serializers.ValidationError("请传递房间类型")
        room_nums = attrs.get("room_nums")
        if not room_nums:
            raise serializers.ValidationError("请传递房间数量")

        #  这里计算价格
        consumer = self.context['request'].user.consumer

        unit_price = room_style.price
        if consumer.is_vip:
            unit_price = unit_price * consumer.vipmember.discount

        attrs.update({"room_price": unit_price})

        return attrs

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style',
            'room_nums',
            'room_price',
            'room_style_name',
            'reserve_check_in_time',
            'reserve_check_out_time',
            'contact_name',
            'contact_phone',
            'days'
        )
        read_only_fields = ('room_price', 'days')


class CreateHotelOrderSerializer(serializers.ModelSerializer):
    hotel_order_detail = CreateHotelOrderDetailSerializer()

    image = serializers.CharField(read_only=True)
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True
    )
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )

    @staticmethod
    def charge_user_balance(hotel_detail, consumer, validated_data):
        # 扣除用户余额。首先扣去充值金额
        # 剩余的钱就是用户本金还有的钱。
        left_money = consumer.recharge_balance - validated_data['order_amount']

        if left_money > 0:
            consumer.recharge_balance = left_money
            recharge_balance = validated_data['order_amount']
            free_balance = 0
            consumer.save()
        else:
            recharge_balance = consumer.recharge_balance
            free_balance = abs(left_money)
            consumer.recharge_balance = 0
            consumer.free_balance = consumer.free_balance + left_money
            consumer.save()

        # 这里记录数据
        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": "余额消费,预定房间:{},数量:{}".format(hotel_detail['room_style'].style_name, hotel_detail['room_nums']),
            "cost_price": -validated_data['order_amount'],
            "left_balance": consumer.balance,
        }
        balance_info = ConsumerBalance(**params)
        balance_info.save()
        # 下单支付成功扣除房间数
        hotel_detail['room_style'].room_count = hotel_detail['room_style'].room_count - hotel_detail['room_nums']
        hotel_detail['room_style'].save()
        return recharge_balance, free_balance

    def validate(self, attrs):
        pay_type = attrs.get("pay_type")
        if not pay_type:
            raise serializers.ValidationError("请传递支付方式")
        if pay_type == PayType.integral:
            raise serializers.ValidationError("不支持积分兑换")

        hotel_order_detail = attrs.get("hotel_order_detail")

        # 验证
        contact_name = hotel_order_detail.get("contact_name") or None
        contact_phone = hotel_order_detail.get("contact_phone") or None
        if not contact_name:
            raise serializers.ValidationError("请传递订单联系姓名")

        if not contact_phone:
            raise serializers.ValidationError("请传递订单联系电话")

        if hotel_order_detail['reserve_check_in_time'] > hotel_order_detail['reserve_check_out_time']:
            raise serializers.ValidationError("入住时间不能够大于退房时间")

        # 计算总价
        order_amount = hotel_order_detail['room_nums'] * hotel_order_detail['room_price']
        num = hotel_order_detail['room_nums']
        attrs.update({"num": num, "order_amount": order_amount})
        return attrs

    @atomic
    def create(self, validated_data):
        consumer = self.context['request'].user.consumer
        # 第一判断支付类型。余额支付时，进行扣除余额并更改支付状态
        validated_data.update({"order_type": OrderType.hotel})
        hotel_order_detail = validated_data.pop("hotel_order_detail")
        pay_info = None
        if validated_data.get("pay_type") == PayType.balance:
            if consumer.balance < validated_data['order_amount']:
                validated_data.update({"order_status": OrderStatus.pre_pay})
            else:
                recharge_balance, free_balance = self.charge_user_balance(hotel_order_detail, consumer, validated_data)

                pay_info = {
                    "free_money": free_balance,
                    "money": recharge_balance
                }
                validated_data.update({"order_status": OrderStatus.to_check_in})
                validated_data.update({"pay_time": datetime.datetime.now()})
        else:
            validated_data.update({"order_status": OrderStatus.pre_pay})

        instance = super(CreateHotelOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        if pay_info:
            pay_info.update({"order": instance})
            OrderPay.objects.create(**pay_info)
        hotel_order_detail.update({"hotel_order": instance})
        HotelOrderDetail.objects.create(**hotel_order_detail)
        return instance

    class Meta:
        model = Order
        fields = (
            'id',
            'hotel_order_detail',
            'belong_hotel',
            'order_id',
            'order_status',
            'order_status_display',
            "create_time",
            "pay_type",
            "pay_type_display",
            "order_amount",
            'num',
            'image',
            'belong_hotel_name',
            'user_remark',
        )
        read_only_fields = (
            'order_id',
            'order_status',
            'order_amount',
            'num',
            'image'
        )


class MarketOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'integral',
            'sale_price',
            'nums',
            'consignee_name',
            'consignee_address',
            'consignee_phone'
        )


class HotelOrderDetailSerializer(serializers.ModelSerializer):
    room_style_name = serializers.CharField(
        source='room_style.style_name',
        read_only=True
    )
    room_style_image = serializers.CharField(
        source='room_style.cover_image',
        read_only=True
    )

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style_name',
            'room_nums',
            'room_style_image',
            'room_price',
            'reserve_check_in_time',
            'reserve_check_out_time',
            'contact_name',
            'contact_phone',
        )


class OrderSerializer(serializers.ModelSerializer):
    hotel_order_detail = HotelOrderDetailSerializer(read_only=True)
    market_order_detail = MarketOrderDetailSerializer(read_only=True)
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True,
    )
    order_type_display = serializers.CharField(
        source='get_order_type_display',
        read_only=True
    )
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True,
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True,
    )
    image = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        order_status = validated_data.get("order_status")
        # 用户申请退款.
        if order_status == OrderStatus.prp_refund and instance.order_status >= OrderStatus.check_in:
            raise serializers.ValidationError({"non_field_errors": ['当前订单无法申请退款']})

        instance = super(OrderSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = Order
        fields = (
            'id',
            'hotel_order_detail',
            'market_order_detail',
            'order_id',
            'order_type',
            'order_type_display',
            'belong_hotel',
            'belong_hotel_name',
            'order_status',
            'order_status_display',
            'pay_type',
            'pay_type_display',
            'num',
            'order_amount',
            'pay_time',
            'create_time',
            'refund_reason',
            'user_remark',
            'image',
        )
        read_only_fields = (
            'order_id',
            'order_type',
            'belong_hotel'
        )


class OrderPayAgainSerializer(serializers.ModelSerializer):
    hotel_order_detail = CreateHotelOrderDetailSerializer(read_only=True)
    market_order_detail = MarketOrderDetailSerializer(read_only=True)

    @staticmethod
    def hotel_charge_user_balance(instance, consumer):
        # 扣除用户余额。首先扣去充值金额
        # 剩余的钱就是用户本金还有的钱。
        hotel_detail = instance.hotel_order_detail
        left_money = consumer.recharge_balance - instance.order_amount
        if left_money > 0:
            consumer.recharge_balance = left_money
            free_balance = 0
            recharge_balance = instance.order_amount
            consumer.save()
        else:

            recharge_balance = consumer.recharge_balance
            free_balance = abs(left_money)
            consumer.recharge_balance = 0
            consumer.free_balance = consumer.free_balance + left_money
            consumer.save()

        # 这里记录数据
        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": "余额消费,预定房间:{},数量:{}".format(hotel_detail.room_style.style_name, hotel_detail.room_nums),
            "cost_price": -instance.order_amount,
            "left_balance": consumer.balance,
        }
        balance_info = ConsumerBalance(**params)
        balance_info.save()
        # 下单扣除房间数
        hotel_detail.room_style.room_count = hotel_detail.room_style.room_count - hotel_detail.room_nums
        hotel_detail.room_style.save()
        return recharge_balance, free_balance

    def validate(self, attrs):
        pay_type = attrs.get("pay_type") or self.instance.pay_type

        if self.instance.order_type == OrderType.hotel and pay_type == PayType.integral:
            raise serializers.ValidationError("支付类型传递错误")

        if self.instance.order_status == OrderStatus.pasted:
            raise serializers.ValidationError("当前订单已过期,请重新下单")
        if self.instance.order_status > OrderStatus.pre_pay:
            raise serializers.ValidationError("当前订单已支付")

        # 这里判断一下时间, 20分钟过期。
        if datetime.datetime.now() - self.instance.create_time > datetime.timedelta(minutes=20):
            self.instance.order_status = OrderStatus.pasted
            self.instance.save()
            raise serializers.ValidationError("当前订单已过期，请重新下单")

        return attrs

    @staticmethod
    def integral_buy(consumer, instance, remark):
        left_integral = consumer.integral - instance.integral
        consumer.integral = left_integral
        consumer.save()
        create_integral_info(consumer, instance.integral, 20, remark)

    @staticmethod
    def market_balance_buy(consumer, instance):
        left_balance = consumer.recharge_balance - instance.order_amount
        free_balance = 0
        if left_balance < 0:
            left_balance = consumer.free_balance + left_balance
            free_balance = abs(left_balance)
            recharge_balance = consumer.recharge_balance
            consumer.recharge_balance = 0
            consumer.free_balance = left_balance
        else:
            consumer.recharge_balance = left_balance
            recharge_balance = instance.order_amount
        consumer.save()

        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": "余额消费,购买商品:{},数量:{}".format(
                instance.market_order_detail.goods_name, instance.market_order_detail.num),
            "cost_price": -instance.order_amount,
            "left_balance": consumer.balance,
        }
        ConsumerBalance(**params).save()

        return recharge_balance, free_balance

    @atomic
    def update(self, instance, validated_data):
        pay_type = validated_data.get("pay_type") or instance.pay_type
        consumer = self.context['request'].user.consumer
        pay_info = None
        if pay_type == PayType.balance and instance.order_type == OrderType.hotel:
            if consumer.balance > instance.order_amount:
                validated_data.update({"order_status": OrderStatus.to_check_in})
                validated_data.update({"pay_time": datetime.datetime.now()})
                recharge_balance, free_balance = self.hotel_charge_user_balance(instance, consumer)
                pay_info = {
                    "free_money": free_balance,
                    "money": recharge_balance,
                }
        elif pay_type == PayType.balance and instance.order_type == OrderType.market:
            if consumer.balance > instance.order_amount:
                validated_data.update({"order_status": OrderStatus.deliver})
                validated_data.update({"pay_time": datetime.datetime.now()})
                recharge_balance, free_balance = self.market_balance_buy(consumer, instance)
                pay_info = {
                    "free_money": free_balance,
                    "money": recharge_balance,
                }
        elif pay_type == PayType.integral and instance.order_type == OrderType.market:
            if consumer.integral > instance.integral:
                validated_data.update({"order_status": OrderStatus.deliver})
                validated_data.update({"pay_time": datetime.datetime.now()})
                remark = "积分消费:购买商品:{},数量:{},单价:{}".format(
                    instance.market_order_detail.goods_name, instance.num, instance.market_order_detail.integral)
                self.integral_buy(consumer, instance, remark)
                pay_info = {
                    "integral": instance.integral
                }
        instance = super(OrderPayAgainSerializer, self).update(instance, validated_data)

        if pay_info:
            pay_info.update({"order": instance})
            logger.info("create pay info :{}".format(pay_info))
            OrderPay.objects.create(**pay_info)
        return instance

    class Meta:
        model = Order
        fields = (
            'id',
            'order_id',
            'order_type',
            'pay_type',
            'hotel_order_detail',
            'market_order_detail',
            'order_amount',
            'order_status',
            'num',
            'integral'
        )
        read_only_fields = (
            'order_amount',
            'order_id',
            'order_status',
            'num',
            'integral'
        )


class CreateMarketOrderDetailSerializer(serializers.ModelSerializer):

    goods_name = serializers.CharField(
        source='goods.goods_name',
        read_only=True
    )

    def validate(self, attrs):
        goods = attrs.get("goods")
        if not goods:
            raise serializers.ValidationError("商品不存在")

        if goods.is_special:
            return attrs

        if not attrs.get("consignee_name"):
            raise serializers.ValidationError("请填写收货人姓名")

        if not attrs.get("consignee_address"):
            raise serializers.ValidationError("请传递收货地址")

        if not attrs.get("consignee_phone"):
            raise serializers.ValidationError("请传递收货人电话")

        return attrs

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'nums',
            'sale_price',
            'goods_name',
            'integral',
            'consignee_name',
            'consignee_address',
            'consignee_phone'
        )
        read_only_fields = ('sale_price', 'integral')


class CreateMarketOrderSerializer(serializers.ModelSerializer):
    market_order_detail = CreateMarketOrderDetailSerializer(required=True)

    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True
    )

    def validate(self, attrs):
        order_detail = attrs['market_order_detail']
        goods = order_detail['goods']

        pay_type = attrs.get("pay_type") or PayType.weixin
        if pay_type == PayType.integral and not goods.is_integral:
            raise serializers.ValidationError("当前商品不支持积分兑换")

        unit_integral = 0  # 积分单价
        unit_price = 0  # 商品单价
        need_price = 0  # 当前用户需要支付金额
        need_integral = 0  # 当前用户需要花费金额

        if pay_type == PayType.integral:
            unit_integral = goods.need_integral
            need_integral = unit_integral * order_detail['nums']
        elif pay_type == PayType.balance:
            unit_price = goods.goods_price
            need_price = unit_price * order_detail['nums']
        else:
            unit_price = goods.goods_price
            need_price = unit_price * order_detail['nums']

        attrs.update({"integral": need_integral, "order_amount": need_price, "num": order_detail['nums']})
        order_detail.update({"sale_price": unit_price, "integral": unit_integral})
        return attrs

    @staticmethod
    def integral_buy(consumer, validated_data):
        # 创建积分消费记录
        left_integral = consumer.integral - validated_data['pay_integral']
        consumer.integral = left_integral
        consumer.save()

    @staticmethod
    def balance_buy(consumer, validated_data, market_order_detail):
        left_balance = consumer.recharge_balance - validated_data['order_amount']
        free_balance = 0
        if left_balance < 0:
            left_balance = consumer.free_balance + left_balance
            free_balance = abs(left_balance)
            recharge_balance = consumer.recharge_balance
            consumer.recharge_balance = 0
            consumer.free_balance = left_balance
        else:
            consumer.recharge_balance = left_balance
            recharge_balance = validated_data['order_amount']
        consumer.save()

        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": "余额消费,购买商品:{},数量:{}".format(
                market_order_detail['goods'].goods_name, market_order_detail['nums']),
            "cost_price": -validated_data['order_amount'],
            "left_balance": consumer.balance,
        }
        ConsumerBalance(**params).save()

        return recharge_balance, free_balance

    @classmethod
    def create_vip(cls, consumer, vip_level):
        params = {
            "consumer": consumer,
            "vip_level": vip_level,
            "vip_no": VipMember.make_vip_no()
        }
        VipMember.objects.create(**params)

    @atomic
    def create(self, validated_data):
        market_order_detail = validated_data.pop('market_order_detail', None)

        # 这里需要计算出本次订单的金额以及积分
        # 步骤1。判断支付类型，
        # 步骤2。积分兑换。
        # 步骤3。余额兑换
        # 步骤4。微信支付
        consumer = self.context['request'].user.consumer
        order_pay_params = {}
        if validated_data['pay_type'] == PayType.integral:
            if consumer.integral < validated_data['integral']:
                validated_data.update({"order_status": OrderStatus.pre_pay})
            else:
                self.integral_buy(consumer, validated_data)
                validated_data.update({"order_status": OrderStatus.deliver})
                validated_data.update({"pay_time": datetime.datetime.now()})

                order_pay_params = {
                    "integral": validated_data['integral']
                }

        elif validated_data['pay_type'] == PayType.balance:

            if consumer.balance > validated_data['order_amount']:
                recharge, free = self.balance_buy(consumer, validated_data, market_order_detail)
                order_pay_params = {
                    "money": recharge,
                    "free_money": free
                }
                validated_data.update({"order_status": OrderStatus.deliver})
                validated_data.update({"pay_time": datetime.datetime.now()})
            else:
                validated_data.update({"order_status": OrderStatus.pre_pay})
        else:
            validated_data.update({"order_status": OrderStatus.pre_pay})

        validated_data.update({"order_type": OrderType.market})
        # 这里是当用户余额支付成功，并且商品是会员。直接开通会员, 并把状态变更为已完成
        if market_order_detail['goods'].is_special and validated_data['order_status'] != OrderStatus.pre_pay:
            validated_data.update({"order_status": OrderStatus.success})
            # 这里创建会员
            level = market_order_detail['goods'].vip_info
            self.create_vip(consumer, level)

        instance = super(CreateMarketOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        if order_pay_params:
            # 创建一条支付信息。只有当成功支付时，才会有支付信息
            order_pay_params.update({"order": instance})
            OrderPay.objects.create(**order_pay_params)
        market_order_detail.update({"market_order": instance})
        MarketOrderDetail.objects.create(**market_order_detail)

        return instance

    class Meta:
        model = Order
        fields = (
            'id',
            'order_id',
            'order_status',
            'order_status_display',
            'pay_type',
            'pay_type_display',
            'pay_time',
            'num',
            'order_amount',
            'integral',
            'user_remark',
            'consumer',
            'market_order_detail',
        )
        read_only_fields = (
            'order_id',
            'order_amount',
            'pay_integral',
            'consumer',
            'num',
            "order_status",
            "pay_time",
            "integral",
        )