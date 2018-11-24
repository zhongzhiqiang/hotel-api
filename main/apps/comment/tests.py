# coding:utf-8
# Time    : 2018/11/6 下午11:08
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from __future__ import unicode_literals

from main.common.base_test import BaseTest


class CommentTest(BaseTest):
    def test_get_base_test(self):
        path = '/user/comment/'
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_post_comment(self):
        path = '/user/comment/'
        post_data = {
            'belong_order': 5,
            "comment_list": [{
                "content": "xxx",
                "comment_level": "5"
            }]
        }
        resp = self.client.post(path, data=post_data, format='json')
        self.assertEqual(resp.status_code, 201)
