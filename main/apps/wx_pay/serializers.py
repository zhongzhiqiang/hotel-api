# coding:utf-8
# Time    : 2018/10/1 下午7:30
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals


from rest_framework import serializers

STATUS_CHOICE = (
    ('market', 'market'),
    ('hotel', 'hotel')
)


class StatusSearchSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    order_type = serializers.ChoiceField(choices=STATUS_CHOICE)

