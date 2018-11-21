# coding:utf-8
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

from main.models import Hotel, RoomStyles, Rooms
from main.apps.admin_hotels import serializers, filters
from main.common.gaode import GaoDeMap
from main.common.permissions import PermsRequired


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
    update_lat_long:
        强制后端更新数据。不需要传递参数.
    """

    serializer_class = serializers.HotelSerializers
    queryset = Hotel.objects.all()
    search_fields = ('name', )
    permission_classes = (PermsRequired('main.hotel'),)

    def perform_create(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        else:
            serializer.save()

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

    @detail_route(methods=['POST'])
    def update_lat_long(self, request, *args, **kwargs):
        instance = self.get_object()
        ret = GaoDeMap().get_lat_longitude(instance.address)
        if ret['status'] == '00000':
            instance.longitude = ret['data'].get('longitude')
            instance.latitude = ret['data'].get('latitude')
            instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


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
    filter_class = filters.RoomStyleFilter
    search_fields = ('style_name', )
    permission_classes = (PermsRequired('main.hotel'),)

    def perform_create(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        else:
            serializer.save()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateRoomStyleSerializer
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
    search_fields = ('room_style__style_name', )
    filter_class = filters.RoomFilter
    permission_classes = (PermsRequired('main.hotel'),)

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
            return serializers.CreateRoomSerializer
        return self.serializer_class
