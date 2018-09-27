# coding:utf-8
# Time    : 2018/9/26 上午11:11
# Author  : Zhongzq
# Site    : 
# File    : defines.py
# Software: PyCharm
from __future__ import unicode_literals


class PayType(object):
    # 支付方式
    integral = 10
    balance = 20
    weixin = 30


class MarketOrderStatus(object):
    unpay = 10
    wait_deliver = 20  # 等待发货
    take_delivery = 30  # 等待收货
    success = 40
    cancel = 50
