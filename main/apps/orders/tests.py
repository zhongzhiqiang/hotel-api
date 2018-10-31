# coding:utf-8
# Time    : 2018/10/31 下午2:25
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest
from main.models import RoomStyles, Order
from main.common.defines import OrderStatus


class OrderTest(BaseTest):
    def test_cancel_market_data(self):
        path = '/user/order/1/refunded/'
        patch_data = {
            "refund_reason": "12345"
        }
        resp = self.client.post(path, patch_data)
        self.assertEqual(resp.status_code, 200)

    def test_cancel_hotel_data(self):
        path = '/user/order/2/refunded/'
        patch_data = {
            "refund_reason": "12345"
        }
        order = Order.objects.get(id=2)
        room_style = RoomStyles.objects.get(id=order.hotel_order_detail.room_style.id)
        room_count = room_style.room_count
        resp = self.client.post(path, patch_data)

        self.assertEqual(resp.status_code, 200)
        order = Order.objects.get(id=2)
        room_style = RoomStyles.objects.get(id=order.hotel_order_detail.room_style.id)
        new_room_count = room_style.room_count
        self.assertEqual(order.order_status, OrderStatus.apply_refund)
        self.assertEqual(room_count + order.num, new_room_count)
