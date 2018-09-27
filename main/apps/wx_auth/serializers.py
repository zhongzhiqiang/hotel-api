# coding:utf-8
# Time    : 2018/9/6 上午9:52
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Consumer


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
        read_only_fields = ('is_distribution', 'sell_user', 'bonus')

