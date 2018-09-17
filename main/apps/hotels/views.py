# coding:utf-8

from rest_framework import mixins, viewsets

from main.models import Hotel
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
        return self.serializer_class
