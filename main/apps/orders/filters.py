# coding:utf-8
# Time    : 2018/10/7 下午11:06
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import Order


class HotelOrderFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Order
        fields = {
            "order_status": ['in', 'exact'],
            "pay_type": ['in', 'exact'],
            "pay_time": ['range'],
            "create_time": ['range'],
            "operator_time": ['range'],
        }
