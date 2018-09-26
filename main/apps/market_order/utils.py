# coding:utf-8
# Time    : 2018/9/26 下午5:18
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals
from weixin.pay import WXAppPay


def unifiedorder(body, out_trade_no, total_fee, openid):
    kwargs = {
        "appid": "",
        "mch_id": "",
        "notify_url": "",
    }
    wx_pay = WXAppPay(**kwargs)
    result = wx_pay.unifiedorder()
    return result
