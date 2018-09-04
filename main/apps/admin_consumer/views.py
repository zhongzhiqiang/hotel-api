# coding:utf-8
# Time    : 2018/9/4 下午10:24
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.admin_consumer import serializers, filters
from main.models import Consumer


class AdminConsumerView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    list:
        返回所有客户
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建数据
    retrieve:
        返回单个数据。查询id为list返回的id
    """

    queryset = Consumer.objects.all()
    serializer_class = serializers.ConsumerSerializer
    filter_class = filters.ConsumerFilter