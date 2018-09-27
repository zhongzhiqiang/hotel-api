# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import serializers
from django.db.transaction import atomic

from main.models import HotelOrder, HotelOrderDetail, Hotel, ConsumerBalance
from main.common.defines import PayType


class CreateHotelOrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelOrderDetail
        fields = (
            'id',
            'room_style',
            'room_nums',
            'room_price',
        )
        read_only_fields = ('room_price', )


class CreateHotelOrderSerializer(serializers.ModelSerializer):
    hotelorderdetail = CreateHotelOrderDetailSerializer()

    def validate(self, attrs):
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

        pay_money = room_price * hotel_detail['room_nums']
        if consumer.balance < pay_money and attrs.get("pay_type") == PayType.balance:
            raise serializers.ValidationError("用户余额不足")
        hotel_detail.update({"room_price": room_price})
        attrs.update({"sale_price": pay_money})
        return attrs

    @atomic
    def create(self, validated_data):
        hotel_detail = validated_data.pop('hotelorderdetail', {})

        pay_type = validated_data.get("pay_type") or PayType.weixin
        consumer = self.context['request'].user.consumer
        # 这里需要判断用户的支付方式
        if pay_type == PayType.balance:
            # 扣除用户余额以及新增用户余额消费明细。
            validated_data.update({"order_status": 20})
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
        )
        read_only_fields = ('order_id', 'order_status', 'room_style_num', 'sale_price')


class HotelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrder
        fields = "__all__"
        depth = 3
