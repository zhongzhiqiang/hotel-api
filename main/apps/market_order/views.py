# coding:utf-8
# Time    : 2018/9/8 下午8:27
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import MarketOrder
from main.apps.market_order import serializers


class MarketOrderViews(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        返回当前用户的所有订单.
        ```
        market_order_detail 字段传递:
        [{"goods_name":"商品名称，从goods获取的goods_name"，
        "sale_price": "销售价格 TODO 这里暂时前端传递。等带后续改进",
        "nums"： "购买数量"}]
        ```
    create:
        创建订单
    update:
        更新数据。
    """
    queryset = MarketOrder.objects.filter().prefetch_related('market_order_detail')
    serializer_class = serializers.MarketOrderSerializer

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)
        return serializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateMarketOrderSerializer
        return self.serializer_class