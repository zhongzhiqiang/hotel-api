# coding:utf-8

from rest_framework import mixins, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from main.models import Hotel, RoomStyles
from main.apps.hotels.serializers import HotelSerializers, RoomStyleSerializer


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

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializers

    @detail_route(methods=['GET'])
    def room_style(self, request, *args, **kwargs):
        instance = self.get_object()
        room_style = RoomStyles.objects.filter(belong_hotel=instance.id)
        serializer = RoomStyleSerializer(instance=room_style, many=True)
        return Response(serializer.data)

