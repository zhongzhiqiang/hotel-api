# coding:utf-8
# Time    : 2018/8/28 上午9:41
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import Rooms, RoomStyles


class RoomStyleFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = RoomStyles
        fields = {
            "style_name": ['exact']
        }


class RoomFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Rooms
        fields = {
            "room_status": ['exact'],
            "room_style__style_name": ['exact']
        }