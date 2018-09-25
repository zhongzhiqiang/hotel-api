# coding:utf-8
# Time    : 2018/9/9 下午9:32
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.hotel_orders import serializers
from main.models import HotelOrder


class HotelOrderViews(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = HotelOrder.objects.all()
    serializer_class = serializers.HotelOrderSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateHotelOrderSerializer
        return self.serializer_class
