# coding:utf-8
# Time    : 2018/9/4 下午10:10
# Author  : Zhongzq
# Site    : 
# File    : perms.py
# Software: PyCharm
from __future__ import unicode_literals

import itertools


permission = [
    {
        "name": "横幅页",
        "codename": "banner"
    }, {
        "name": "宾馆中心",
        "codename": "hotel"
    }, {
        "name": "客户中心",
        "codename": "consumer"
    }, {
        "name": "权限中心",
        "codename": "role"
    }, {
        "name": "分销中心",
        "codename": "distribution",
    }, {
        "name": "积分中心",
        "codename": "integral",
    }, {
        "name": "商城中心",
        "codename": "market"
    }, {
        "name": "商城订单中心",
        "codename": "market_order"
    }, {
        "name": "标签中心",
        "codename": "tags"
    }, {
        "name": "职员中心",
        "codename": "staff"
    }, {
        "name": "住宿订单",
        "codename": "hotel_order"
    }
]

ALL_PERMS = list(itertools.chain.from_iterable([
    [(perm['codename'], perm['name']) for perm in permission]]))
