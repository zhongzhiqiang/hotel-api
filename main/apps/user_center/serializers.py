# coding:utf-8
# Time    : 2018/9/5 下午9:53
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
    sell_user_name = serializers.CharField(
        source='sell_user.user_name'
    )
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )
    email = serializers.CharField(
        source='user.email',
        allow_blank=True
    )

    class Meta:
        model = Consumer
        fields = (
            'id',
            'sex',
            'sex_display',
            'phone',
            'user_name',
            'contact_addr',
            'is_distribution',
            'sell_user',
            'bonus',
            'email',
            'username'  # 这个为登录账号
        )