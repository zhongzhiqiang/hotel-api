# coding:utf-8
# Time    : 2018/9/26 下午5:18
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals
from weixin.pay import WXAppPay

from main.common.wx_config import WXConfig


def unifiedorder(out_trade_no, total_fee, openid, detail):
    total_fee = int(float(total_fee) * 100)
    kwargs = {
        "body": '曼嘉酒店-商场',
        "out_trade_no": out_trade_no,
        "total_fee": total_fee,
        "openid": openid,
        "detail": detail,

    }
    wx_pay = WXAppPay(WXConfig.APP_ID, WXConfig.MCH_ID)
    result = wx_pay.unifiedorder(**kwargs)
    return result
