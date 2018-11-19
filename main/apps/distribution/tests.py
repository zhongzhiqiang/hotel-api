# coding:utf-8
# Time    : 2018/11/19 上午9:36
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest


class DistributionTest(BaseTest):

    def test_pick(self):
        path = '/user/pick_bonus/'
        post_data = {
            "pick_money": 20,
        }
        resp = self.client.post(path, post_data)
        self.assertEqual(resp.status_code, 201)
