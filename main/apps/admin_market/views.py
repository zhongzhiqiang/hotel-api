# coding:utf-8

from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.admin_market import serializers, filters
from main.models import Goods, GoodsCategory
from main.common.permissions import PermsRequired


class GoodsCategoryView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    list:
        返回商品分类
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建商品分类
    retrieve:
        返回单个商品分类。查询id为list返回的id
    """

    def perform_create(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    queryset = GoodsCategory.objects.all()
    serializer_class = serializers.GoodsCategorySerializer
    permission_classes = (PermsRequired('main.market'), )

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateGoodsCategorySerializer
        return self.serializer_class


class GoodsView(mixins.CreateModelMixin,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """
    list:
        返回所有商品
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建商品
        ```
        创建会员商品时,需要传递is_special字段为True，并且选择会员权益传递.
        ```
    retrieve:
        返回单个商品。查询id为list返回的id
    """

    queryset = Goods.objects.all()
    filter_class = filters.AdminGoodsFilter
    serializer_class = serializers.GoodsSerializer
    permission_classes = (PermsRequired('main.market'),)

    def perform_create(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateGoodsSerializer
        return self.serializer_class
