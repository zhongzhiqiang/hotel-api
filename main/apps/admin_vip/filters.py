# coding:utf-8
# Time    : 2018/10/12 下午11:12
# Author  : Zhongzq
# Site    : 
# File    : filters.py
# Software: PyCharm
from __future__ import unicode_literals

import django_filters

from main.models import VipMember


class VipMemberFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = VipMember
        fields = {
            "vip_no": ['exact', 'contains']
        }
