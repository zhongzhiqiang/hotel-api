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


class CreateApplySerializer(serializers.ModelSerializer):
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
            'fail_remark'
        )


class CreateBonusPickSerializer(serializers.ModelSerializer):
    # TODO 需要做限制

    def create(self, validated_data):
        instance = super(CreateBonusPickSerializer, self).create(validated_data)
        instance.order_id = instance.make_order_id()
        instance.save()
        return instance

    class Meta:
        model = DistributionBonusPick
        fields = (
            'pick_money',
        )
