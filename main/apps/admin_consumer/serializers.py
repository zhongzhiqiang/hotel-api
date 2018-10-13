# coding:utf-8
# Time    : 2018/9/4 下午10:20
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):

    sex_display = serializers.CharField(
        source='get_sex_display',
        read_only=True
    )
    user_account = serializers.CharField(
        source='user.username',
        read_only=True
    )
    sell_user_name = serializers.CharField(
        source='sell_user.user_name',
        default='',
        read_only=True
    )

    class Meta:
        model = Consumer
        fields = (
            'id',
            'user_id',
            "phone",
            "user_name",
            'user_account',
            "sex",
            "sex_display",
            'contact_addr',
            'is_distribution',
            'sell_user_name',
            'user_account',
            'bonus',
            'is_vip',
            'discount',
            'integral'
        )
