# coding:utf-8
# Time    : 2018/11/9 上午9:16
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals


from main.common.base_test import BaseTest


class MarketTest(BaseTest):
    def test_get_market(self):
        path = '/user/goods_list/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)