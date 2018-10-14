# coding:utf-8
# Time    : 2018/10/14 下午9:04
# Author  : Zhongzq
# Site    : 
# File    : filter.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import HotelOrderComment


class OrderCommentFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = HotelOrderComment
        fields = {
            "belong_order__order_type": ['exact'],
            "comment_show": ['exact'],
            "comment_level": ['exact', 'in'],
            'is_reply': ['exact']
        }
