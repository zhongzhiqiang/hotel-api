# coding:utf-8
# Time    : 2018/9/6 上午9:52
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Consumer, ConsumerBalance, RechargeInfo, RechargeSettings


class WeiXinCreateTokenSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=100, help_text='微信登录获取code')


class WeiXinDataDecrypt(serializers.Serializer):
    encrypt_data = serializers.CharField(help_text='微信加密数据')
    iv = serializers.CharField(help_text='向量')


class ConsumerSerializer(serializers.ModelSerializer):
    sex_display = serializers.CharField(
        source='get_sex_display',
        read_only=True
    )
    sell_user_name = serializers.CharField(
        source='sell_user.user_name',
        read_only=True
    )

    class Meta:
        model = Consumer
        fields = (
            'id',
            'phone',
            'user_name',
            'sex',
            'contact_addr',
            'is_distribution',
            'sell_user',
            'sex_display',
            'bonus',
            'sell_user',
            'sell_user_name',
            'balance',
            'recharge_balance',
            'free_balance'
        )
        read_only_fields = ('is_distribution', 'sell_user', 'bonus', 'free_balance', 'recharge_balance')


class ConsumerBalanceSerializer(serializers.ModelSerializer):
    # 用户余额详情
    balance_type_display = serializers.CharField(
        source='get_balance_type_display',
        read_only=True
    )

    class Meta:
        model = ConsumerBalance
        fields = (
            'id',
            'balance_type',
            'balance_type_display',
            'message',
            'cost_price',
            'create_time',
            'left_balance'
        )


class CreateRechargeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        recharge_money = validated_data["recharge_money"]
        discount = RechargeSettings.objects.filter(recharge_price=recharge_money).first()
        if not discount:
            raise serializers.ValidationError("充值金额错误")
        validated_data.update({"free_money": discount.free_balance})
        instance = super(CreateRechargeSerializer, self).create(validated_data)
        instance.order_id = instance.make_order()
        instance.save()
        return instance

    class Meta:
        model = RechargeInfo
        fields = (
            'id',
            'order_id',
            'recharge_money',
            'free_money'
        )
        read_only_fields = ("free_money", )


class RechargeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RechargeInfo
        fields = "__all__"


class RechargeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeSettings
        fields = "__all__"