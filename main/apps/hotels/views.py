# coding:utf-8

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.db.models import Q

from main.models import Hotel, HotelOrderComment
from main.apps.hotels.serializers import HotelSerializers, HotelDetailSerializer


class HotelView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """
    list:
        返回所有旅馆信息
    retrieve:
        获取单个宾馆信息
    room_style:
        返回宾馆的所有房间信息
    """

    queryset = Hotel.objects.filter(is_active=True).prefetch_related('room_styles')
    serializer_class = HotelSerializers
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HotelDetailSerializer
        elif self.action == 'comment':
            return ''
        return self.serializer_class

    def get_queryset(self):
        if self.action == 'comment':
            return HotelOrderComment.objects.all()
        return self.queryset

    # @list_route(methods=['GET'])
    # def comment(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    @detail_route(methods=['GET'])
    def comment(self, request, *args, **kwargs):
        self.get_object()
        query_params = Q(comment_show=20) & Q()
        if hasattr(self.request.user, 'consumer'):
            query_params = query_params | Q(commenter=self.request.user.consumer)

        HotelOrderComment.objects.filter()