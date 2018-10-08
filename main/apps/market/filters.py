# coding:utf-8

import django_filters

from main.models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Goods
        fields = {
            'category': ['exact'],
            "is_promotion": ['exact']
        }
