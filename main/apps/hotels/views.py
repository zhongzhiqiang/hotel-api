# coding:utf-8

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from django.db.models import Q, Avg

from main.models import Hotel, HotelOrderComment
from main.apps.hotels.serializers import HotelSerializers, HotelDetailSerializer, HotelCommentSerializer


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
    comment:
        返回当前宾馆的评论。
        传递宾馆的ID
    """

    queryset = Hotel.objects.filter(is_active=True).prefetch_related('room_styles')
    serializer_class = HotelSerializers
    permission_classes = ()

    def get_authenticators(self):
        if self.action_map['get'] != 'comment':
            self.authentication_classes = ()
        return super(HotelView, self).get_authenticators()

    def get_paginated_response(self, data, meta={}):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, meta)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HotelDetailSerializer
        elif self.action == 'comment':
            return HotelCommentSerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action == 'comment':
            return HotelOrderComment.objects.all()
        return self.queryset

    @detail_route(methods=['GET'])
    def comment(self, request, *args, **kwargs):
        lookup_fields = self.lookup_url_kwarg or self.lookup_field

        query_params = Q(comment_show=20)
        if hasattr(self.request.user, 'consumer'):
            query_params = (query_params | Q(commenter=self.request.user.consumer))

        query_params = query_params & Q(belong_order__belong_hotel__id=kwargs[lookup_fields]) & Q(belong_order__order_type=20)

        queryset = HotelOrderComment.objects.filter(query_params).prefetch_related('comment_reply')
        tmp = queryset.aggregate(level_avg=Avg('comment_level'))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data, meta=tmp)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
