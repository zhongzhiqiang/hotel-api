# coding:utf-8
# Time    : 2018/9/26 下午9:47
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.admin_marketorder import serializers
from main.models import MarketOrder


class MarketOrderView(mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    
    """
    serializer_class = serializers.MarketOrderSerializer
    queryset = MarketOrder.objects.all()
