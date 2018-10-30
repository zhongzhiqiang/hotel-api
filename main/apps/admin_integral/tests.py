# coding:utf-8
# Time    : 2018/10/30 下午10:05
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest


class IntegralTest(BaseTest):
    def test_user_integral(self):
        path = '/admin/integral/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_user_detail_integral(self):
        path = '/admin/integral/1/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)