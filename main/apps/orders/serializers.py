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

from main.models import (Order, HotelOrderDetail, ConsumerBalance, OrderType, MarketOrderDetail, VipMember, OrderPay,
                         IntegralDetail, MarketOrderContact, MarketOrderExpress, Cart)
from main.common.defines import PayType, OrderStatus
from main.common.utils import create_integral_info
from main.common import utils
from main.schedul.tasks import cancel_task
from main.common.constant import CANCEl_TIME
logger = logging.getLogger('django')


class MarketOrderExpressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrderExpress
        fields = "__all__"


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
        now = datetime.datetime.now()
        unit_price = room_style.price
        # # TODO。特交房处理
        # if room_style.is_promotion and room_style.promotion_start < now < room_style.promotion_end:
        #     unit_price = room_style.promotion_price

        if consumer.is_vip:
            unit_price = unit_price * consumer.discount

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

    order_type_display = serializers.CharField(
        source='get_order_type_display',
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
        # 这里判断用户是否还有未支付的订单。如果有返回无法下单.
        order = Order.objects.filter(consumer=consumer, order_type=OrderType.hotel, order_status=OrderStatus.pre_pay).first()
        if order:
            raise serializers.ValidationError({"non_field_errors": ['已有未支付订单,无法在创建']})
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

        # 创建订单
        instance = super(CreateHotelOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()

        if pay_info:
            pay_info.update({"order": instance})
            OrderPay.objects.create(**pay_info)
        hotel_order_detail.update({"hotel_order": instance})
        HotelOrderDetail.objects.create(**hotel_order_detail)
        cancel_task.apply_async(args=(instance.order_id, ), countdown=CANCEl_TIME)
        # 下单成功，扣除房间数
        utils.reduce_room_num(instance.hotel_order_detail.room_style, instance.num)

        return instance

    class Meta:
        model = Order
        fields = (
            'id',
            'hotel_order_detail',
            'belong_hotel',
            'order_id',
            'order_status',
            'order_type',
            'order_type_display',
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
            'order_type',
            'order_amount',
            'num',
            'image'
        )


class MarketOrderDetailSerializer(serializers.ModelSerializer):
    is_integral = serializers.BooleanField(
        source='goods.is_integral',
        read_only=True
    )

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'goods_integral',
            'goods_price',
            'nums',
            'cover_image',
            'is_integral'
        )


class MarketOrderContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrderContact
        fields = "__all__"


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
            'days',
            'image'
        )


class OrderSerializer(serializers.ModelSerializer):
    hotel_order_detail = HotelOrderDetailSerializer(read_only=True)
    market_order_detail = MarketOrderDetailSerializer(many=True)
    market_order_contact = MarketOrderContactSerializer(read_only=True)
    order_express = MarketOrderExpressSerializer(read_only=True)
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

    @atomic
    def update(self, instance, validated_data):
        order_status = validated_data.get("order_status")
        # 用户申请退款.
        if order_status == OrderStatus.pre_refund and instance.order_status >= OrderStatus.check_in:
            raise serializers.ValidationError({"non_field_errors": ['当前订单无法申请退款']})

        # 如果用户申请退款，将房间数直接减去。
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
            'market_order_contact',
            'integral',
            'order_express'
        )
        read_only_fields = (
            'order_id',
            'order_type',
            'integral'
            'order_express',
            'belong_hotel'
        )


class OrderPayAgainSerializer(serializers.ModelSerializer):
    hotel_order_detail = CreateHotelOrderDetailSerializer(read_only=True)
    market_order_detail = MarketOrderDetailSerializer(read_only=True, many=True)

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
            "message": u"余额消费,预定房间:{},数量:{}".format(hotel_detail.room_style.style_name, hotel_detail.room_nums),
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
        consumer.integral_info.integral = left_integral
        consumer.integral_info.save()
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

        goods_name, nums = utils.get_goods_name_by_instance(instance.market_order_detail, 'market')
        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": "余额消费,购买商品:{},数量:{}".format(goods_name, instance.market_order_detail.num),
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
        # 重新支付需要判断用户类型。
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
            # 首先判断是否有积分
            if consumer.integral < instance.integral:
                raise serializers.ValidationError({"non_field_error": ['用户积分不足']})

            if consumer.balance > instance.order_amount:
                validated_data.update({"order_status": OrderStatus.deliver})
                validated_data.update({"pay_time": datetime.datetime.now()})
                recharge_balance, free_balance = self.market_balance_buy(consumer, instance)
                pay_info = {
                    "free_money": free_balance,
                    "money": recharge_balance,
                }
                if instance.integral > 0:
                    self.integral_buy(consumer, instance, '消费,购买商品')
                    pay_info.update({"integral": instance.integral})
            # TODO 这里需要把购物车的相应商品给删除

        instance = super(OrderPayAgainSerializer, self).update(instance, validated_data)

        # 这里需要判断是否为会员商品并且支付成功的
        if instance.order_type == OrderType.market and instance.order_status == OrderStatus.deliver:
            for market_order in instance.market_order_detail.all():
                if market_order.is_special:
                    utils.create_vip(instance.consumer, market_order.vip_info)

        if pay_info:
            pay_info.update({"order": instance})
            # logger.info("create pay info :{}".format(pay_info))
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


class CreateMarketOrderContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketOrderContact
        fields = "__all__"


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

        return attrs

    class Meta:
        model = MarketOrderDetail
        fields = (
            'id',
            'goods',
            'nums',
            'goods_price',
            'goods_name',
            'goods_integral',
            'is_integral',
            'cover_image'
        )
        read_only_fields = ('goods_price', 'goods_integral', 'is_integral', 'cover_image')


class CreateMarketOrderSerializer(serializers.ModelSerializer):
    market_order_detail = CreateMarketOrderDetailSerializer(required=True, many=True)
    market_order_contact = CreateMarketOrderContactSerializer(required=True)
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True
    )
    order_type_display = serializers.CharField(
        source='get_order_type_display',
        read_only=True
    )

    def validate(self, attrs):
        market_order_detail_list = attrs['market_order_detail'] or []
        market_order_contact = attrs.get("market_order_contact") or {}
        if not market_order_contact:
            raise serializers.ValidationError("请传递订单联系信息")

        for k, v in market_order_contact.items():
            if not v:
                raise serializers.ValidationError("请传递完整传递联系")

        if len(market_order_detail_list) < 1:
            raise serializers.ValidationError("请传递商品信息")

        consumer = self.context['request'].user.consumer

        # 循环遍历。计算
        need_integral = 0  # 需要的积分
        need_price = 0  # 需要的金钱
        nums = 0
        vip_count = 0  # 购买的会员数量
        vip_obj = None
        for market_order_detail in market_order_detail_list:
            goods = market_order_detail['goods']
            nums += market_order_detail['nums']
            if goods.is_special:
                vip_count += 1
                vip_obj = market_order_detail
            if goods.is_integral:
                need_integral += (goods.need_integral * market_order_detail['nums'])
                market_order_detail.update({"goods_integral": goods.need_integral})

            if not goods.is_integral:
                need_price += (goods.goods_price * market_order_detail['nums'])
                market_order_detail.update({"goods_price": goods.goods_price})

        # 这里判断会员类型的数量
        if vip_count > 1:
            raise serializers.ValidationError("只能够购买一个会员类型")

        if vip_obj and vip_obj['nums'] != 1:
            raise serializers.ValidationError("会员只能够购买一个")

        if hasattr(consumer, 'vipmember'):
            if vip_obj and vip_obj['goods'].vip_info.vip_weight <= consumer.vipmember.vip_level.vip_weight:
                raise serializers.ValidationError("只能够购买比当前会员等级高的会员类型")

        if vip_count == 1 and len(market_order_detail_list) > 1:
            raise serializers.ValidationError("会员不能够与其他商品购买")

        # 这里判断是否有积分商品
        if consumer.integral < need_integral:
            raise serializers.ValidationError("积分不足, 无法支付")

        pay_type = attrs.get("pay_type")

        if pay_type == PayType.balance:
            if consumer.balance < need_price:
                raise serializers.ValidationError("余额不足,请充值后在支付")

        attrs.update({"integral": need_integral, "order_amount": need_price, "num": nums})

        return attrs

    def integral_buy(self, consumer, validated_data, market_order_detail):
        # 减去用户积分
        left_integral = consumer.integral - validated_data['integral']
        consumer.integral_info.integral = left_integral
        consumer.integral_info.save()

        goods_name, num = utils.get_goods_name_by_post(market_order_detail, 'integral')
        params = {
            "consumer": consumer,
            "integral": -validated_data['integral'],
            "integral_type": 20,
            "remark": u'积分购买商品:{}, 数量:{}'.format(goods_name, num),
            "left_integral": consumer.integral
        }
        IntegralDetail.objects.create(**params)

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
        goods_name, num = utils.get_goods_name_by_post(market_order_detail, 'market')
        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": u"余额消费,购买商品,商品名称:{}, 数量:{}".format(goods_name, num),
            "cost_price": -validated_data['order_amount'],
            "left_balance": consumer.balance,
        }
        ConsumerBalance(**params).save()

        return recharge_balance, free_balance

    @atomic
    def create(self, validated_data):
        market_order_detail = validated_data.pop('market_order_detail', None)
        market_order_contact = validated_data.pop('market_order_contact', None)
        # 这里需要计算出本次订单的金额以及积分
        # 步骤1。判断支付类型
        # 步骤3。余额兑换
        # 步骤4。微信支付
        consumer = self.context['request'].user.consumer
        order = Order.objects.filter(consumer=consumer, order_type=OrderType.market,
                                     order_status=OrderStatus.pre_pay).first()

        order_pay_params = None

        if order:
            raise serializers.ValidationError({"non_field_errors": ['已有未支付订单,无法在创建']})

        if validated_data['pay_type'] == PayType.balance:
            if consumer.balance > validated_data['order_amount']:
                recharge, free = self.balance_buy(consumer, validated_data, market_order_detail)
                order_pay_params = {
                    "money": recharge,
                    "free_money": free,
                    "integral": validated_data['integral']
                }
                validated_data.update({"order_status": OrderStatus.deliver})
                validated_data.update({"pay_time": datetime.datetime.now()})
                if validated_data['integral']:
                    # 创建积分消费记录
                    self.integral_buy(consumer, validated_data, market_order_detail)
            else:
                validated_data.update({"order_status": OrderStatus.pre_pay})
        else:
            validated_data.update({"order_status": OrderStatus.pre_pay})

        validated_data.update({"order_type": OrderType.market})
        # 这里是当用户余额支付成功，并且商品是会员。直接开通会员, 并把状态变更为已完成
        # 这里需要循环创建
        if validated_data['order_status'] != OrderStatus.pre_pay:
            for detail in market_order_detail:
                if detail['goods'].is_special:
                    validated_data.update({"order_status": OrderStatus.success})
                    level = detail['goods'].vip_info
                    utils.create_vip(consumer, level)

        instance = super(CreateMarketOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()

        if order_pay_params:
            # 创建一条支付信息。只有当成功支付时，才会有支付信息
            order_pay_params.update({"order": instance})
            OrderPay.objects.create(**order_pay_params)

        for market_order in market_order_detail:
            market_order.update({"market_order": instance})
            MarketOrderDetail.objects.create(**market_order)
        market_order_contact.update({"order": instance})
        MarketOrderContact.objects.create(**market_order_contact)

        # 这里删除用户的购物车.
        Cart.objects.filter(consumer=consumer).delete()
        cancel_task.apply_async(args=(instance.order_id,), countdown=CANCEl_TIME)
        return instance

    class Meta:
        model = Order
        fields = (
            'id',
            'order_id',
            'order_status',
            'order_status_display',
            'pay_type',
            'order_type',
            'order_type_display',
            'pay_type_display',
            'pay_time',
            'num',
            'order_amount',
            'integral',
            'user_remark',
            'consumer',
            'market_order_detail',
            'market_order_contact'
        )
        read_only_fields = (
            'order_id',
            'order_amount',
            'integral',
            'consumer',
            'order_type',
            'num',
            "order_status",
            "pay_time"
        )


class RefundedOrderSerializer(serializers.ModelSerializer):
    hotel_order_detail = HotelOrderDetailSerializer(read_only=True)
    market_order_detail = MarketOrderDetailSerializer(many=True, read_only=True)
    market_order_contact = MarketOrderContactSerializer(read_only=True)
    order_express = MarketOrderExpressSerializer(read_only=True)
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

    def validate(self, attrs):

        if not attrs.get("refund_reason"):
            raise serializers.ValidationError("请传递退款原因")

        attrs.update({"order_status": OrderStatus.pre_refund})
        return attrs

    @atomic
    def update(self, instance, validated_data):
        order_status = validated_data.get("order_status")
        # 用户申请退款.
        if order_status == OrderStatus.pre_refund and instance.order_status >= OrderStatus.check_in:
            raise serializers.ValidationError({"non_field_errors": ['当前订单无法申请退款']})

        # 判断是否为商场订单且为会员
        market_order_detail = self.instance.market_order_detail

        if self.instance.order_type == OrderType.market:
            for market in market_order_detail:
                if market.is_special:
                    raise serializers.ValidationError({"non_field_errors": ['特殊商品无法退款']})
        # 如果用户申请退款，将房间数直接减去。
        # 判断订单类型。如果是房间，则直接增加房子类型相应的数量
        if instance.order_type == OrderType.hotel:
            utils.increase_room_num(instance)
        instance = super(RefundedOrderSerializer, self).update(instance, validated_data)
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
            'market_order_contact',
            'order_express',
            'integral'
        )
        read_only_fields = (
            'order_id',
            'order_type',
            'belong_hotel',
            'hotel_order_detail',
            'market_order_detail',
            'belong_hotel',
            'pay_type',
            'num',
            'order_amount',
            'pay_time',
            'user_remark',
            'market_order_contact',
            'order_express',
            'integral'
        )
