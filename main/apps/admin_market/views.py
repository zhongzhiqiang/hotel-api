# coding:utf-8

from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.admin_market import serializers, filters
from main.models import Goods, GoodsCategory


class GoodsCategoryView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.all()
    serializer_class = serializers.GoodsCategorySerializer


class GoodsView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    queryset = Goods.objects.all()
    filter_class = filters.AdminGoodsFilter
    serializer_class = serializers.GoodsSerializer
