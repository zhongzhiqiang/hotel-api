# coding:utf-8
# Time    : 2018/10/3 下午3:46
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from django.db import transaction
from main.models import RechargeSettings, RechargeInfo


class FormatDecimalField(serializers.DecimalField):
    def to_representation(self, value):
        value = '{:g}'.format(float(value))
        return value


class RechargeSettingsSerializer(serializers.ModelSerializer):

    free_balance = FormatDecimalField(max_digits=10, decimal_places=2)
    recharge_price = FormatDecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = RechargeSettings
        fields = (
            "id",
            "free_balance",
            "recharge_price",
        )


class CreateRechargeSerializer(serializers.ModelSerializer):

    recharge_settings_id = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        recharge_settings_id = attrs.pop("recharge_settings_id")
        setting = RechargeSettings.objects.filter(id=recharge_settings_id, is_active=True).first()
        if not setting:
            raise serializers.ValidationError("充值金额有误,请重新输入")
        attrs.update({"free_money": setting.free_balance, "recharge_money": setting.recharge_price})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("recharge_settings_id", '')
        validated_data.update({"recharge_status": 30})
        instance = super(CreateRechargeSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        return instance

    class Meta:
        model = RechargeInfo
        fields = (
            "id",
            'order_id',
            "recharge_money",
            "free_money",
            'recharge_settings_id',
            'balance'
        )
        read_only_fields = (
            'free_money',
            "order_id",
            "recharge_money"
        )


class RechargeSerializer(serializers.ModelSerializer):
    recharge_status_display = serializers.CharField(
        source='get_recharge_status_display',
        read_only=True
    )

    class Meta:
        model = RechargeInfo
        fields = (
            "id",
            "order_id",
            "recharge_money",
            "free_money",
            "consumer",
            "create_time",
            "update_time",
            "pay_time",
            "recharge_status",
            'recharge_status_display',
            'balance'
        )
        read_only_fields = ("order_id", "recharge_money", "free_money", "pay_time")


class RechargePayAgainSerializer(serializers.ModelSerializer):

    recharge_status_display = serializers.CharField(
        source='get_recharge_status_display',
        read_only=True
    )

    def validate(self, attrs):
        if self.instance.recharge_status != 30:
            raise serializers.ValidationError("当前订单状态非等待支付")

        return attrs

    class Meta:
        model = RechargeInfo
        fields = (
            'id',
            'order_id',
            'recharge_money',
            'free_money',
            'consumer',
            'create_time',
            "update_time",
            "pay_time",
            "recharge_status",
            'recharge_status_display',
            'balance'
        )
        read_only_fields = ("order_id", "recharge_money", "free_money", "pay_time", 'recharge_status')


class RechargeCancelSerializer(serializers.ModelSerializer):
    recharge_status_display = serializers.CharField(
        source='get_recharge_status_display',
        read_only=True
    )

    def validate(self, attrs):
        recharge_status = attrs.get('recharge_status')
        if recharge_status != 20:
            raise serializers.ValidationError("订单状态传递错误")

        if self.instance.recharge_status != 30:
            raise serializers.ValidationError("当前订单不能够取消")

        return attrs

    class Meta:
        model = RechargeInfo
        fields = (
            'id',
            'order_id',
            'recharge_money',
            'free_money',
            'consumer',
            'create_time',
            "update_time",
            "pay_time",
            "recharge_status",
            'recharge_status_display',
            'balance'
        )
        read_only_fields = ("order_id", "recharge_money", "free_money", "pay_time")