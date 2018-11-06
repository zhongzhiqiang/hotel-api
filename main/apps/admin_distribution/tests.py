# coding:utf-8
# Time    : 2018/11/6 下午9:38
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest


class DistributionTest(BaseTest):

    def test_get_distribution_list(self):
        path = '/admin/apply/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_patch_distribution(self):
        path = '/admin/apply/1/'
        patch_data = {
            "apply_status": 30
        }
        resp = self.client.put(path, data=patch_data)
        self.assertEqual(resp.status_code, 200)

    def test_patch_distribution_fail(self):
        path = '/admin/apply/1/'
        patch_data = {
            "apply_status": 20,
            "fail_remark": "xxx"
        }
        resp = self.client.put(path, data=patch_data)
        self.assertEqual(resp.status_code, 200)

