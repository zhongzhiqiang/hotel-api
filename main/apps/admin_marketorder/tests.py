# coding:utf-8
# Time    : 2018/10/30 下午10:19
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest
from main.common.defines import OrderStatus


class MarketOrderTest(BaseTest):

    def test_get_market_order_list(self):
        path = '/admin/market_order/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_patch_markket_order(self):
        path = '/admin/market_order/1/'
        patch_data = {
            "order_status": OrderStatus.take_deliver,
            "order_express": {
                "express_id": "1234567",
                "express_name": "12345"
            }
        }
        resp = self.client.patch(path, patch_data, format='json')
        self.assertEqual(resp.status_code, 200)