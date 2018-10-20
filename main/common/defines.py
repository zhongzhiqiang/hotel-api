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


class WeiXinCode(object):
    success = 'SUCCESS'
    fail = 'FAIL'
    error = "ERROR"


class OrderStatus(object):
    pre_pay = 10
    deliver = 15
    take_deliver = 20
    to_check_in = 25
    check_in = 30
    success = 35  # 成功未评价
    finish = 40  # 结束
    canceled = 45

    pre_refund = 50
    refund_ing = 55
    refunded = 60
    pasted = 65
    deleted = 70


class OrderType(object):
    market = 10
    hotel = 20


class RefundedStatus(object):
    refunded_ing = 10
    success = 20
    fail = 30
    retry = 40
    unknown = 50

