# coding:utf-8

from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.market.serializers import GoodsCategorySerializer, GoodsSerializer
from main.models import GoodsCategory, Goods
from main.apps.market.filters import GoodsFilter


class GoodsList(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_active=True).prefetch_related('goods')
    serializer_class = GoodsCategorySerializer


class GoodsCategoryView(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(is_active=True)
    serializer_class = GoodsCategorySerializer


class GoodsView(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    queryset = Goods.objects.filter(is_active=True)
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter
