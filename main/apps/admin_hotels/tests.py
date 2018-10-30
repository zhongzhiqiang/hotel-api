# coding:utf-8
# Time    : 2018/10/30 下午9:49
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest


class HotelTest(BaseTest):

    def test_list_hotel(self):
        path = '/admin/hotel/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['count'], 1)

    def test_post_hotel(self):
        path = '/admin/hotel/'
        post_data = {
            "name": "测试333",
            "province": "四川省",
            "city": "成都市",
            "area": "双流区",
            "street": "天府大道南端651号",
            "hotel_profile": "哈哈哈哈",
        }
        resp = self.client.post(path, data=post_data)
        self.assertEqual(resp.status_code, 201)

    def test_post_room_style(self):
        path = '/admin/room_style/'
        post_data = {
            "belong_hotel": 1,
            "style_name": "高端房间333",
            "price": "100",
            "room_profile": "hhhh"
        }
        resp = self.client.post(path, post_data)
        self.assertEqual(resp.status_code, 201)

    def test_list_room_style(self):
        path = '/admin/room_style/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)
