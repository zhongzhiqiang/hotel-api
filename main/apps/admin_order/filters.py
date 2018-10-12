# coding:utf-8
# Time    : 2018/9/1 下午1:56
# Author  : Zhongzq
# Site    : 
# File    : filter.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import Order


class HotelOrderFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Order
        fields = {
            "order_status": ['exact', 'in'],
            "order_amount": ['in'],
            'pay_time': ['range'],
            'consumer__user_name': ['exact'],
        }
