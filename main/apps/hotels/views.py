# coding:utf-8

from rest_framework import mixins, viewsets

from main.models import Hotel
from main.apps.hotels.serializers import HotelSerializers


class HotelView(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializers
