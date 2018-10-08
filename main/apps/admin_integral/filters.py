# coding:utf-8
# Time    : 2018/10/8 下午8:46
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import IntegralDetail, IntegralSettings


class IntegralDetailFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = IntegralDetail
        fields = {
            "integral_type": ['exact'],
            "create_time": ['range'],
        }


class IntegralSettingsFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = IntegralSettings
        fields = {
            "create_time": ['range']
        }
