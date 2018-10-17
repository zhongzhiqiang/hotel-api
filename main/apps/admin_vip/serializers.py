# coding:utf-8
# Time    : 2018/9/25 下午10:12
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from main.models import VipMember, VipSettings


class VipSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VipSettings
        fields = (
            'id',
            'vip_name',
            'hotel_discount',
            'operator_name',
            'vip_weight'
        )
        read_only_fields = ('operator_name', )
        extra_kwargs = {
            'vip_weight': {
                'validators': [
                    UniqueValidator(VipSettings.objects.all(), message=u'已有该权重'),
                ],
                'error_messages': {
                    'null': u'请填写权重',
                    'blank': u'请填写权重',
                    'required': u'请填写权重',
                }
            },
        }


class VipMemberSerializer(serializers.ModelSerializer):
    vipsettings = VipSettingsSerializer(read_only=True)

    consumer_name = serializers.CharField(
        source='consumer.user_name',
        read_only=True,
    )
    consumer_url = serializers.HyperlinkedIdentityField(view_name='consumer-detail')

    vip_level_name = serializers.CharField(
        source='vip_level.vip_name',
        read_only=True,
    )

    class Meta:
        model = VipMember
        fields = (
            'id',
            'vip_no',
            'consumer',
            'consumer_id',
            'vip_level',
            'consumer_name',
            'consumer_url',
            'vipsettings',
            'create_time',
            'discount',
            'vip_level_name'
        )
