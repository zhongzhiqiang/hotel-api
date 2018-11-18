# coding:utf-8
# Time    : 2018/10/31 下午2:25
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest
from main.models import RoomStyles, Order, Goods
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

    def test_post_market_data(self):
        path = '/user/order/market_order_create/'
        post_data = {
            "market_order_detail": [{
                "goods": "1",
                "nums": "10",
            }],
            "pay_type": "20",
            "user_remark": "s32323233",
            "market_order_contact": {
                "consignee_name": "3233223",
                "consignee_address": "收货人地址",
                "consignee_phone": "收货人电话"
            }
        }
        resp = self.client.post(path, data=post_data, format='json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        order = Order.objects.get(id=data['id'])
        goods = Goods.objects.get(id=1)
        self.assertEqual(order.num, 10)
        price = goods.goods_price * order.num
        self.assertEqual(order.order_amount, price)

    def test_post_hotel_data(self):
        path = '/user/order/'

        post_data = {
            "pay_type": "20",
            "belong_hotel": "1",
            "hotel_order_detail": {
                "room_style": "1",
                "room_nums": "10",
                "reserve_check_in_time": "2018-09-10",
                "reserve_check_out_time": "2018-09-11",
                "contact_name": "22",
                "contact_phone": "33",
            },
            "user_remark": "33"
        }
        resp = self.client.post(path, post_data, format='json')
        self.assertEqual(resp.status_code, 200)

    def test_refunded_hotel(self):
        path = "/user/order/2/refunded/"
        patch_data = {
            "refund_reason": "xxxx"
        }
        resp = self.client.post(path, data=patch_data, format='json')
        self.assertEqual(resp.status_code, 200)

    def test_fill_market(self):
        path = '/user/order/4/market_fill_refunded/'
        patch_data = {
            "user_refunded_info": {
                "user_express_id": "xxx",
                "user_express": "1234",
                "remark": "1234"
            }
        }
        resp = self.client.post(path, data=patch_data, format='json')
        self.assertEqual(resp.status_code, 200)

    def test_delivery_market(self):
        path = '/user/order/7/market_delivery/'
        resp = self.client.post(path)
        self.assertEqual(resp.status_code, 200)

    def test_list_data(self):
        path = '/user/order/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)
