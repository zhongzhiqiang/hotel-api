# coding:utf-8
# Time    : 2018/11/8 下午5:36
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals
import django_filters

from main.models import Order


class OrderFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Order
        fields = {
            "order_status": ['exact', 'in']
        }