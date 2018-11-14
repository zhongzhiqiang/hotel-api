# coding:utf-8
# Time    : 2018/10/30 下午9:43
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals


from main.common.base_test import BaseTest


class AdminConsumrTest(BaseTest):

    def test_consumer(self):
        path = '/admin/consumer/'

        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)