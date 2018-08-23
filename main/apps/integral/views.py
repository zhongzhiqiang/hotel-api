# coding:utf-8
# Time    : 2018/8/23 下午9:29
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route

from main.apps.integral import serializers
from main.models import Integral, IntegralDetail


class UserIntegralView(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        返回当前用户的积分
    integral_detail:
        返回当前用户的积分详情
    """

    queryset = Integral.objects.all()
    serializer_class = serializers.IntegralSerializer

    def get_queryset(self):
        user = self.request.user
        consumer = getattr(user, 'consumer', None)
        if consumer:
            return self.queryset.filter(user=consumer)
        return self.queryset

    @list_route(methods=['GET'])
    def integral_detail(self, request, *args, **kwargs):
        # 获取当前用户等积分明细
        user = self.request.user
        consumer = getattr(user, 'consumer', None)
        if consumer:

            queryset = IntegralDetail.objects.filter(consumer=consumer)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = serializers.IntegralDetailSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = serializers.IntegralDetailSerializer(instance=page, many=True)
            return Response(serializer.data)
        return Response([])
