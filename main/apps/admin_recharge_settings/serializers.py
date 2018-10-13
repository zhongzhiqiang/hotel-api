# coding:utf-8
# Time    : 2018/10/3 下午3:47
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from main.models import RechargeSettings, RechargeInfo


class RechargeSettingsSerializer(serializers.ModelSerializer):

    # def validate(self, attrs):
    #     min_price = attrs.get("min_price")
    #     max_price = attrs.get("max_price")
    #     if not min_price:
    #         raise serializers.ValidationError("请传递最小金额")
    #     if not max_price:
    #         raise serializers.ValidationError("请传递最大金额")
    #
    #     if min_price > max_price:
    #         raise serializers.ValidationError("请最大金额必须大于最小金额")

    def create(self, validated_data):
        count = RechargeSettings.objects.all().count()
        if count >= 6:
            raise serializers.ValidationError({"non_field_errors": ['充值优惠已经有6个']})

        instance = super(RechargeSettingsSerializer, self).create(validated_data)
        return instance

    class Meta:
        model = RechargeSettings
        fields = "__all__"
        read_only_fields = ("operator_name", )
        validators = [
            UniqueTogetherValidator(
                queryset=RechargeSettings.objects.all(),
                fields=('free_balance', 'recharge_price'),
                message='已有相同配置'
            )
        ]


class RechargeInfoSerializer(serializers.ModelSerializer):
    recharge_status_display = serializers.CharField(
        source='get_recharge_status_display',
        read_only=True
    )
    consumer_name = serializers.CharField(
        source='consumer.user_name',
        read_only=True
    )

    class Meta:
        model = RechargeInfo
        fields = (
            'id',
            'order_id',
            'recharge_status_display',
            'recharge_status',
            'recharge_money',
            'free_money',
            'consumer',
            'consumer_name',
            'create_time',
            'pay_time',
            'update_time'
        )
