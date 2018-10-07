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


class RechargeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeSettings
        fields = (
            "id",
            "free_balance",
            "recharge_price",
        )


class CreateRechargeSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        recharge_money = attrs.get("recharge_money")
        setting = RechargeSettings.objects.filter(
            recharge_price=recharge_money, is_active=True).first()
        if not setting:
            raise serializers.ValidationError("充值金额有误,请重新输入")
        attrs.update({"free_money": setting.free_balance})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
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
            "free_money"
        )
        read_only_fields = (
            'free_money',
            "order_id"
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
            'recharge_status_display'
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
        )
        read_only_fields = ("order_id", "recharge_money", "free_money", "pay_time")