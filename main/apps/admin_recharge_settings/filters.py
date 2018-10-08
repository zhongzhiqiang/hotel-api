# coding:utf-8
# Time    : 2018/10/8 下午8:51
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import RechargeInfo


class RechargeInfoFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = RechargeInfo
        fields = {
            "order_id": ['exact', 'contains'],
            "recharge_status": ['exact', 'in']
        }
