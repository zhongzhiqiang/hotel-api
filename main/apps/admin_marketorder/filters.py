# coding:utf-8
# Time    : 2018/10/12 上午12:35
# Author  : Zhongzq
# Site    : 
# File    : filter.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import Order


class OrderFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Order
        fields = {
            "order_status": ['exact', 'in'],
            "create_time": ['range'],
            "pay_type": ['exact', 'in'],
            "pay_time": ['range']
        }
