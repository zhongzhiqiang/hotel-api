# coding:utf-8
# Time    : 2018/9/1 下午1:45
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals

from main.models import IntegralDetail, IntegralInfo


def get_integral(money):

    return int(money) * 1  # 1:1
    # raise TypeError("未添加配置")


def make_integral(consumer, integral, remark):
    if not hasattr(consumer, 'integral_info'):
        IntegralInfo.objects.create(user=consumer)
    consumer.integral_info.integral = consumer.integral_info.integral + integral
    consumer.integral_info.growth_value = consumer.integral_info.growth_value + integral
    consumer.integral_info.save()
    params = {
        "consumer": consumer,
        "integral": integral,
        "integral_type": 10,
        "remark": remark,
        "left_integral": consumer.integral_info.integral,
    }
    IntegralDetail.objects.create(**params)
