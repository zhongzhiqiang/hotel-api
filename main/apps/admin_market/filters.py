# coding:utf-8
from __future__ import unicode_literals

import django_filters

from main.models import Goods


class AdminGoodsFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Goods
        fields = {
            'category': ['exact']
        }
