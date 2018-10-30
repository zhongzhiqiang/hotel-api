# coding:utf-8
# Time    : 2018/10/30 下午10:36
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals
from main.common.base_test import BaseTest
from main.common.defines import OrderStatus


class HotelOrderTest(BaseTest):

    def test_list_order(self):
        path = '/admin/hotel_order/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_patch_order(self):
        # 测试用户住宿。
        path = '/admin/hotel_order/2/'
        patch_data = {
            "order_status": OrderStatus.to_check_in,
            "operator_remark": "哈哈哈哈"

        }
        resp = self.client.patch(path, patch_data)
        self.assertEqual(resp.status_code, 200)