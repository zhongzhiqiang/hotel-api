# coding:utf-8
# Time    : 2018/8/30 下午8:43
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime
import logging


from rest_framework import serializers
from django.db import transaction

from main.models import DistributionBonusPick, DistributionBonusDetail, DistributionApply

logger = logging.getLogger(__name__)


class ApplySerializer(serializers.ModelSerializer):

    consumer_name = serializers.CharField(
        source='consumer.user_name',
        read_only=True
    )

    apply_status_display = serializers.CharField(
        source="get_apply_status_display",
        read_only=True
    )

    @transaction.atomic
    def update(self, instance, validated_data):
        apply_status = validated_data.pop('is_success', False)
        fail_remark = validated_data.pop('fail_remark', '')
        if apply_status:
            # 如果申请状态为成功。则需要将consumer的is_distribution设置为True
            instance.consumer_name.is_distribution = True
            instance.consumer_name.save()

        if apply_status is False and not fail_remark:
            raise serializers.ValidationError("失败时,必须填写失败原因")

        instance = super(ApplySerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = DistributionApply
        fields = (
            'id',
            'consumer_name',
            'consumer',
            'apply_status',
            'apply_status_display',
            'apply_time',
            'apply_remark',
            'fail_remark',
            'is_success'
        )
        read_only_fields = ('consumer', )


class BonusPickSerializer(serializers.ModelSerializer):
    pick_status_display = serializers.CharField(
        source='get_pick_status_display',
        read_only=True
    )
    consumer_name = serializers.CharField(
        source='consumer.user_name',
        read_only=True
    )

    @staticmethod
    def create_bonus_detail(**kwargs):
        instance = DistributionBonusDetail.objects.create(**kwargs)
        logger.info("create bonus detail:{}, instance:{}".format(kwargs, instance))

    @transaction.atomic
    def update(self, instance, validated_data):
        pick_status = validated_data.get('pick_status', None)
        if instance.pick_status == 40 and pick_status == 40:
            raise serializers.ValidationError({"pick_status": ['当前提取申请已转账成功']})
        remark = "提取金额:{}, ".format(instance.pick_money)

        if pick_status and pick_status == 50:
            remark += '失败'
            kwargs = {
                "status": "20",
                "pick": instance,
                "last_bonus": instance.consumer.bonus,
                "use_bonus": -instance.pick_money,
                "consumer": instance.consumer,
                "remark": remark,
                'detail_type': 20,  # 支出
            }
            self.create_bonus_detail(**kwargs)

            raise serializers.ValidationError("提取失败时，需要输入失败原因")
        elif pick_status and pick_status == 30:
            validated_data.update({"transfer_time": datetime.datetime.now()})
        elif pick_status and pick_status == 40:
            # 这里需要把提取明细更改为成功
            last_bonus = instance.consumer.bonus - instance.pick_money
            if last_bonus < 0:
                logger.info("consumer pick:{}, last lte 0".format(instance.consumer.user_name))
                raise serializers.ValidationError({"pick_money": ['提取金额超出限制']})
            remark += '成功'
            kwargs = {
                "status": "20",
                "pick": instance,
                "last_bonus": last_bonus,
                "use_bonus": -instance.pick_money,
                "consumer": instance.consumer,
                "remark": remark,
                "detail_type": 20,
            }
            self.create_bonus_detail(**kwargs)
            # 将关联用户的
            instance.consumer.bonus = last_bonus
            instance.consumer.save()
            validated_data.update({"success_time": datetime.datetime.now()})

        instance = super(BonusPickSerializer, self).update(instance, validated_data)
        return instance

    class Meta:
        model = DistributionBonusPick
        fields = (
            'id',
            'consumer_name',
            'pick_status',
            'pick_status_display',
            'pick_money',
            'pick_time',
            'success_time'
        )

        read_only_fields = ('pick_money', 'pick_time', 'success_time')
