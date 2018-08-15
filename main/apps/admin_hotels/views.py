# coding:utf-8
from __future__ import unicode_literals

from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route

from main.models import Hotel
from main.apps.admin_hotels import serializers
from main.common.gaode import GaoDeMap


class AdminHotelView(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

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
