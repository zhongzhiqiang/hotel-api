# coding:utf-8
# Time    : 2018/8/29 下午9:56
# Author  : Zhongzq
# Site    : 
# File    : serializer.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import DistributionApply, DistributionBonusDetail, DistributionBonus, DistributionBonusPick


class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionApply
        fields = "__all__"


class CreateApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionApply
        fields = (
            'apply_remark',
        )


class DistributionBonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionBonus
        fields = (
            'bonus'
        )


class DistributionBonusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionBonusDetail
        fields = "__all__"


class BonusPickSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionBonusPick
        fields = "__all__"


class CreateBonusPickSerializer(serializers.ModelSerializer):
    # TODO 需要做限制
    class Meta:
        model = DistributionBonusPick
        fields = (
            'pick_money',
        )
