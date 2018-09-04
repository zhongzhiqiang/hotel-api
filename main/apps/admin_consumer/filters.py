# coding:utf-8
# Time    : 2018/9/4 下午10:24
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import Consumer


class ConsumerFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Consumer
        fields = {
            'is_distribution': ['exact'],
            'user__date_joined': ['range'],
            'user_name': ['contains'],
            'phone': ['contains'],
            'sex': ['exact']
        }

