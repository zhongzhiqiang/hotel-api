# coding:utf-8
# Time    : 2018/9/1 下午1:45
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals

from main.models import IntegralSettings


def get_integral(money):
    integral_settings = IntegralSettings.objects.all().first()
    if integral_settings:
        return money * integral_settings.ratio
    raise TypeError("未添加配置")
