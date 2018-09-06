# coding:utf-8

from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.market.serializers import GoodsCategorySerializer, GoodsSerializer
from main.models import GoodsCategory, Goods
from main.apps.market.filters import GoodsFilter


class GoodsList(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """
    list:
        返回商品列表
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建商品分类
    retrieve:
        返回单个商品分类。查询id为list返回的id
    """
    queryset = GoodsCategory.objects.filter(is_active=True).prefetch_related('goods')
    serializer_class = GoodsCategorySerializer
    permission_classes = ()
    authentication_classes = ()


class GoodsCategoryView(mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    list:
        返回商品分类信息
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建商品分类
    retrieve:
        返回单个商品分类。查询id为list返回的id
    """

    queryset = GoodsCategory.objects.filter(is_active=True)
    serializer_class = GoodsCategorySerializer
    permission_classes = ()
    authentication_classes = ()


class GoodsView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """
    list:
        返回商品信息
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建商品分类
    retrieve:
        返回单个商品。查询id为list返回的id
    """

    queryset = Goods.objects.filter(is_active=True)
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter
    permission_classes = ()
    authentication_classes = ()
