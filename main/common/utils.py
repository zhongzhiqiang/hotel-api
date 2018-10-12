# coding:utf-8
# Time    : 2018/9/26 下午5:00
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals
from main.models import IntegralDetail


def create_balance_info(user, integral, integral_type, remark):
    # 生成用户余额详情。
    params = {
        "consumer": user,
        "integral": integral,
        "integral_type": integral_type,
        "remark": remark,
    }


def create_integral_info(consumer, integral, integral_type, remark):
    params = {
        "consumer": consumer,
        "integral": integral,
        "remark": remark,
        "integral_type": integral_type,
        "left_integral": consumer.integral
    }
    IntegralDetail.objects.create(**params)
