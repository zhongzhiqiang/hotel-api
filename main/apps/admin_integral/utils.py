# coding:utf-8
# Time    : 2018/9/1 下午1:45
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals

from main.models import IntegralSettings, IntegralDetail, Integral


def get_integral(money):
    integral_settings = IntegralSettings.objects.all().first()
    if integral_settings:
        return money * integral_settings.ratio
    raise TypeError("未添加配置")


def make_integral(consumer, integral, remark):
    if not hasattr(consumer, 'integral'):
        Integral.objects.create(user=consumer)
    consumer.integral.integral = consumer.integral.integral + integral
    consumer.integral.growth_value = consumer.integral.growth_value + integral
    consumer.integral.save()
    params = {
        "consumer": consumer,
        "integral": integral,
        "integral_type": 10,
        "remark": remark,
        "left_integral": consumer.integral.integral,
    }
    IntegralDetail.objects.create(**params)
