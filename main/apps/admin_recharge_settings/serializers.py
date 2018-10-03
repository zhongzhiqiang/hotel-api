# coding:utf-8
# Time    : 2018/10/3 下午3:47
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import RechargeSettings


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

    class Meta:
        model = RechargeSettings
        fields = "__all__"
        read_only_fields = ("operator_name", )
