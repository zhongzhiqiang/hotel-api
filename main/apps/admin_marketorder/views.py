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
    list:
        返回所有的信息
        ```
        订单状态对应的数字。
         ORDER_STATUS = (
        (10, '未支付'),
        (20, '待发货'),
        (30, '待收货'),
        (40, '已完成'),
        (50, '已取消'),
        (60, '等待评价'),
        (70, '评价完成')  # 评价完成后才有积分
    )
        ```
    update:
        更新状态。
    retrieve:
        详情
    """
    serializer_class = serializers.MarketOrderSerializer
    queryset = MarketOrder.objects.all()
