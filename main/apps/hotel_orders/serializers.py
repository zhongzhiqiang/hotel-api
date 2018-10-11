# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime

from rest_framework import serializers
from django.db.transaction import atomic

from main.models import HotelOrder, HotelOrderDetail, Hotel, ConsumerBalance
from main.common.defines import PayType, HotelOrderStatus


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

        return attrs

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style',
            'room_nums',
            'room_price',
            'room_style_name'
        )
        read_only_fields = ('room_price', )


class CreateHotelOrderSerializer(serializers.ModelSerializer):
    hotelorderdetail = CreateHotelOrderDetailSerializer()

    def validate(self, attrs):
        contact_name = attrs.get("contact_name") or None
        contact_phone = attrs.get("contact_phone") or None
        if not contact_name:
            raise serializers.ValidationError("请传递订单联系姓名")

        if not contact_phone:
            raise serializers.ValidationError("请传递订单联系电话")

        # 这里如果用户使用余额支付，需要判断余额是否足够
        consumer = self.context['request'].user.consumer
        hotel_detail = attrs.get('hotelorderdetail')
        if not hotel_detail:
            raise serializers.ValidationError("请填写房间")
        room_style = hotel_detail['room_style']
        sale_price = room_style.price

        if consumer.is_vip:
            room_price = sale_price * 0.8
        else:
            room_price = sale_price

        if attrs['reserve_check_in_time'] > attrs['reserve_check_out_time']:
            raise serializers.ValidationError("入住时间不能够大于退房时间")
        days = (attrs['reserve_check_out_time'] - attrs['reserve_check_in_time']).days

        pay_money = room_price * hotel_detail['room_nums'] * days

        if hotel_detail['room_nums'] > hotel_detail['room_style'].room_count:
            raise serializers.ValidationError("房间数不足")
        hotel_detail.update({"room_price": room_price})
        attrs.update({"sale_price": pay_money})
        return attrs

    @staticmethod
    def charge_user_balance(hotel_detail, consumer, validated_data):
        # 扣除用户余额。首先扣去充值金额
        # 剩余的钱就是用户本金还有的钱。
        left_money = consumer.recharge_balance - validated_data['sale_price']
        if left_money > 0:
            consumer.recharge_balance = left_money
            consumer.save()
        else:
            consumer.recharge_balance = 0
            free_balance = consumer.free_balance - left_money
            consumer.free_balance = free_balance
            consumer.save()

        # 这里记录数据
        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": "余额消费,预定房间:{},数量:{}".format(hotel_detail['room_style'].style_name, hotel_detail['room_nums']),
            "cost_price": -validated_data['sale_price'],
            "left_balance": consumer.balance,
        }
        balance_info = ConsumerBalance(**params)
        balance_info.save()
        # 下单扣除房间数
        hotel_detail['room_style'].room_count = hotel_detail['room_style'].room_count - hotel_detail['room_nums']
        hotel_detail['room_style'].save()

    @atomic
    def create(self, validated_data):

        hotel_detail = validated_data.pop('hotelorderdetail', {})

        pay_type = validated_data.get("pay_type") or PayType.weixin
        consumer = self.context['request'].user.consumer

        validated_data.update({"room_style_num": hotel_detail['room_nums']})
        # 这里需要判断用户的支付方式
        if pay_type == PayType.balance:
            # 扣除用户余额以及新增用户余额消费明细。
            # 这里判断是否足够，如果不足够只生成订单并返回支付失败。
            if consumer.balance > validated_data['sale_price']:
                validated_data.update({"order_status": 20})
                validated_data.update({"pay_time": datetime.datetime.now()})
                self.charge_user_balance(hotel_detail, consumer, validated_data)
            else:
                validated_data.update({"order_status": 10})

        else:
            validated_data.update({"order_status": 10})  # 等待支付
        instance = super(CreateHotelOrderSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()

        hotel_detail_obj = HotelOrderDetail(belong_order=instance, **hotel_detail)
        hotel_detail_obj.save()
        return instance

    class Meta:
        model = HotelOrder
        fields = (
            'id',
            'order_id',
            'order_status',
            'room_style_num',
            'sale_price',
            'reserve_check_in_time',
            'reserve_check_out_time',
            'user_remark',
            'belong_hotel',
            'pay_type',
            'hotelorderdetail',
            'pay_type',
            'contact_name',
            'contact_phone',
        )
        read_only_fields = ('order_id', 'order_status', 'room_style_num', 'sale_price')


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
            'room_price'
        )


class HotelOrderSerializer(serializers.ModelSerializer):
    hotelorderdetail = HotelOrderDetailSerializer()
    hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True,
    )
    order_status_display = serializers.CharField(
        source='get_order_status_display',
        read_only=True,
    )
    pay_type_display = serializers.CharField(
        source='get_pay_type_display',
        read_only=True,
    )

    def update(self, instance, validated_data):
        order_status = validated_data.get("order_status")
        # 用户申请退款.
        if order_status == HotelOrderStatus.refund_to_be and instance.order_status >= HotelOrderStatus.check_in:
            raise serializers.ValidationError({"non_field_errors": ['当前订单无法申请退款']})

        instance = super(HotelOrderSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = HotelOrder
        fields = (
            'id',
            'hotelorderdetail',
            'order_id',
            'belong_hotel',
            'hotel_name',
            'order_status',
            'order_status_display',
            'pay_type',
            'pay_type_display',
            'room_style_num',
            'sale_price',
            'reserve_check_in_time',
            'reserve_check_out_time',
            'pay_time',
            'create_time',
            'refund_reason',
            'user_remark',
            'days',
            'contact_phone',
            'contact_name'
        )


class HotelOrderPayAgainSerializer(serializers.ModelSerializer):
    hotelorderdetail = CreateHotelOrderDetailSerializer(read_only=True)

    @staticmethod
    def charge_user_balance(instance, consumer):
        # 扣除用户余额。首先扣去充值金额
        # 剩余的钱就是用户本金还有的钱。
        hotel_detail = instance.hotelorderdetail
        left_money = consumer.recharge_balance - instance.sale_price
        if left_money > 0:
            consumer.recharge_balance = left_money
            consumer.save()
        else:
            consumer.recharge_balance = 0
            free_balance = consumer.free_balance - left_money
            consumer.free_balance = free_balance
            consumer.save()

        # 这里记录数据
        params = {
            "consumer": consumer,
            "balance_type": 20,
            "message": "余额消费,预定房间:{},数量:{}".format(hotel_detail.room_style.style_name, hotel_detail.room_nums),
            "cost_price": -instance.sale_price,
            "left_balance": consumer.balance,
        }
        balance_info = ConsumerBalance(**params)
        balance_info.save()
        # 下单扣除房间数
        hotel_detail.room_style.room_count = hotel_detail.room_style.room_count - hotel_detail.room_nums
        hotel_detail.room_style.save()

    def validate(self, attrs):
        if self.instance.order_status == 90:
            raise serializers.ValidationError("当前订单已过期,请重新下单")
        if self.instance.order_status >= 20:
            raise serializers.ValidationError("当前订单已支付")

        # 这里判断一下时间, 20分钟过期。
        if datetime.datetime.now() - self.instance.create_time > datetime.timedelta(minutes=20):
            self.instance.order_status = 90
            self.instance.save()
            raise serializers.ValidationError("当前订单已过期，请重新下单")
        return attrs

    @atomic
    def update(self, instance, validated_data):
        pay_type = validated_data.get("pay_type") or instance.pay_type
        consumer = self.context['request'].user.consumer

        if pay_type == PayType.balance:
            if consumer.balance > instance.sale_price:
                validated_data.update({"order_status": 20})
                validated_data.update({"pay_time": datetime.datetime.now()})
                self.charge_user_balance(instance, consumer)
            else:
                validated_data.update({"order_status": 10})
        instance = super(HotelOrderPayAgainSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = HotelOrder
        fields = (
            'id',
            'order_id',
            'pay_type',
            'hotelorderdetail',
            'sale_price',
            'order_status'
        )
        read_only_fields = ('sale_price', 'order_id', 'order_status')
