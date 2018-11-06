# coding:utf-8
# Time    : 2018/8/29 下午9:56
# Author  : Zhongzq
# Site    : 
# File    : serializer.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import DistributionApply, DistributionBonusDetail, DistributionBonusPick


class ApplySerializer(serializers.ModelSerializer):
    apply_status_display = serializers.CharField(
        source='get_apply_status_display',
        read_only=True
    )

    class Meta:
        model = DistributionApply
        fields = (
            'id',
            'apply_status',
            'apply_status_display',
            'apply_remark',
            'success_time',
            'operator_time',
            'is_success',
            'fail_remark',
        )
        read_only_fields = (
            'success_time',
            "is_success",
            "fail_remark",
            "operator_time"
        )


class CreateApplySerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        consumer = self.context['request'].user.consumer
        dist = DistributionApply.objects.filter(consumer=consumer, apply_status=20).first()
        if dist:
            raise serializers.ValidationError("已有申请")
        dist = DistributionApply.objects.filter(consumer=consumer, apply_status=30).first()
        if dist:
            raise serializers.ValidationError("已经成功申请")
        return attrs

    class Meta:
        model = DistributionApply
        fields = (
            'apply_remark',
        )


class DistributionBonusDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    detail_type_display = serializers.CharField(
        source='get_detail_type_display',
        read_only=True,
    )

    class Meta:
        model = DistributionBonusDetail
        fields = (
            'id',
            'status',
            'status_display',
            'detail_type',
            'detail_type_display',
            'pick',
            'last_bonus',
            'use_bonus',
            'remark',
            'create_time',
            'operator_time'
        )


class BonusPickSerializer(serializers.ModelSerializer):
    pick_status_display = serializers.CharField(
        source='get_pick_status_display',
        read_only=True
    )
    transfer_type_display = serializers.CharField(
        source='get_transfer_type_display',
        read_only=True
    )

    def validate(self, attrs):
        transfer_type = attrs.get('transfer_type') or self.instance.transfer_type
        bank = attrs.get('bank') or self.instance.bank
        transfer_account = attrs.get('transfer_account') or self.transfer_account
        pick_money = attrs.get("pick_money") or self.instance.pick_money
        if not pick_money:
            raise serializers.ValidationError("请传递提取金额")
        if not transfer_account:
            raise serializers.ValidationError("请传递转账账号")

        if transfer_type == 30 and not bank:
            raise serializers.ValidationError("银行卡转账时, 请输入开户行")
        consumer = self.context['request'].user.consumer
        if consumer.bonus < pick_money:
            raise serializers.ValidationError("分销奖金不足, 请重新输入")
        if self.instance.pick_status == 30 and attrs.get("pick_money"):
            raise serializers.ValidationError("当前订单无法重新输入金额")

        if self.instance.pick_status == 30 and attrs.get("transfer_account"):
            raise serializers.ValidationError("当前订单无法重新更改转账账号")
        return attrs

    class Meta:
        model = DistributionBonusPick
        fields = (
            'id',
            'pick_status',
            'pick_status_display',
            'pick_order',
            'pick_money',
            'pick_time',
            'success_time',
            'transfer_time',
            'fail_remark',
            'transfer_type',
            'transfer_account',
            'bank',
            'transfer_type_display'
        )
        read_only_fields = ("pick_status", 'pick_order', 'pick_time', 'success_time', 'transfer_time', 'fail_remark')


class CreateBonusPickSerializer(serializers.ModelSerializer):
    # TODO 需要做限制

    def validate(self, attrs):
        transfer_type = attrs.get('transfer_type') or 10
        bank = attrs.get('bank')
        transfer_account = attrs.get('transfer_account')
        pick_money = attrs.get("pick_money")
        if not pick_money:
            raise serializers.ValidationError("请传递提取金额")
        if not transfer_account:
            raise serializers.ValidationError("请传递转账账号")

        if transfer_type == 30 and not bank:
            raise serializers.ValidationError("银行卡转账时, 请输入开户行")
        consumer = self.context['request'].user.consumer
        if consumer.bonus < pick_money:
            raise serializers.ValidationError("分销奖金不足, 请重新输入")
        return attrs

    def create(self, validated_data):
        instance = super(CreateBonusPickSerializer, self).create(validated_data)
        instance.pick_order = instance.make_order_id()
        instance.save()
        return instance

    class Meta:
        model = DistributionBonusPick
        fields = (
            'pick_money',
            'transfer_type',
            'transfer_account',
            'bank',
            "pick_order",
        )
        read_only_fields = ('pick_order', )
