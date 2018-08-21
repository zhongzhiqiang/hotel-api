# coding:utf-8

from rest_framework import mixins, viewsets

from main.models import Hotel
from main.apps.hotels.serializers import HotelSerializers


class HotelView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """
    list:
        返回所有旅馆信息
    partial_update:
        更新部分字段
    update:
        更新某个数据
    create:
        创建商品分类
    retrieve:
        获取某个宾馆详细信息。
    """

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializers
