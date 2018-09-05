# coding:utf-8
# Time    : 2018/9/5 下午9:20
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import Banners


class BannersFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Banners
        fields = {
            'banner_title': ['contains'],
            "is_show": ['exact'],
            "update_time": ['range']
        }
