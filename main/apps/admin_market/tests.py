# coding:utf-8
# Time    : 2018/10/30 下午10:10
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest


class MarketTest(BaseTest):
    def test_category_post_data(self):
        path = '/admin/goods_category/'
        post_data = {
            "category_name": "测试数据",
            "is_active": True
        }
        resp = self.client.post(path, post_data)
        self.assertEqual(resp.status_code, 201)

    def test_category_list(self):
        path = '/admin/goods_category/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 1)

    def test_goods_post(self):
        path = '/admin/goods/'
        post_data = {
            "category": 1,
            "goods_name": "测试333",
            "goods_price": 100,
            "is_integral": False,
            "is_promotion": False,
            "is_active": True
        }
        resp = self.client.post(path, post_data)
        self.assertEqual(resp.status_code, 201)

    def test_goods_list(self):
        path = '/admin/goods/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 2)