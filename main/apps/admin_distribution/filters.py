# coding:utf-8
# Time    : 2018/8/30 下午9:05
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import DistributionApply


class ApplyFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = DistributionApply
        fields = {
            "apply_status": ['in', 'exact'],
            "apply_time": ['range'],
            "is_success": ['exact']
        }