# coding:utf-8
# Time    : 2018/10/31 下午2:25
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest


class OrderTest(BaseTest):
    def test_cancel_data(self):
        path = ''
        patch_data = {
            "resaon":
        }
        resp = self.client.patch(path, patch_data)
        self.assertEqual(resp.status_code, 200)