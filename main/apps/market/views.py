# coding:utf-8

from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from django.db.models import Q, Avg

from main.apps.market.serializers import GoodsCategorySerializer, GoodsSerializer, HotelCommentSerializer
from main.models import GoodsCategory, Goods, HotelOrderComment
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
    comment:
        返回商品的评价。传递商品的ID
    """

    queryset = Goods.objects.filter(is_active=True)
    serializer_class = GoodsSerializer
    filter_class = GoodsFilter
    permission_classes = ()

    def get_paginated_response(self, data, meta={}):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, meta)

    def get_serializer_class(self):
        if self.action == 'comment':
            return HotelCommentSerializer
        return self.serializer_class

    @list_route(methods=['GET'])
    def comment(self, request, *args, **kwargs):
        query_params = Q(comment_show=20)
        if hasattr(self.request.user, 'consumer'):
            query_params = (query_params | Q(commenter=self.request.user.consumer))

        queryset = HotelOrderComment.objects.filter(query_params).prefetch_related('comment_reply')

        tmp = queryset.aggregate(level_avg=Avg('comment_level'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data, meta=tmp)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
