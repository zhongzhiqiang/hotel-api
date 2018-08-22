# coding:utf-8
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from main.models import Hotel, RoomStyles, Rooms
from main.apps.admin_hotels import serializers
from main.common.gaode import GaoDeMap


class AdminHotelView(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    get_lat_long:
        返回经纬度
    list:
        返回所有的宾馆信息
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建数据
    retrieve:
        返回单个数据。查询id为list返回的id
    """

    serializer_class = serializers.HotelSerializers
    queryset = Hotel.objects.all()
    permission_classes = ()

    def get_serializer_class(self):
        if self.action == 'get_lat_long':
            return serializers.AddressSerializers
        elif self.action == 'create':
            return serializers.CreateHotelSerializers
        return self.serializer_class

    @list_route(methods=['POST'])
    def get_lat_long(self, request):
        # 通过address获取经纬度
        serializer = self.get_serializer_class()
        serializer = serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.data['address']

        ret = GaoDeMap().get_lat_longitude(address)
        if ret['status'] == '00000':

            return Response(status=status.HTTP_200_OK, data=ret['data'])
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error_message": "请求错误"})


class AdminRoomStyle(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """

    list:
        返回所有的房间类型信息
    partial_update:
        更新房间部分字段
    update:
        更新某个房间数据，需要传递所有字段
    create:
        创建房间类型数据
    retrieve:
        返回单个数据。查询id为list返回的id
    """
    queryset = RoomStyles.objects.all()
    serializer_class = serializers.RoomStyleSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateHotelSerializers
        return self.serializer_class


class AdminRoomView(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    list:
        返回所有的房间信息
    partial_update:
        更新房间部分字段
    update:
        更新某个房间数据，需要传递所有字段
    create:
        创建房间类型数据
    retrieve:
        返回单个数据。查询id为list返回的id
    """

    queryset = Rooms.objects.all()
    serializer_class = serializers.RoomSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateRoomSerializer
        return self.serializer_class
