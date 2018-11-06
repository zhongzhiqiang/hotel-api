# coding:utf-8
# Time    : 2018/10/30 下午9:45
# Author  : Zhongzq
# Site    : 
# File    : base_test.py
# Software: PyCharm

from rest_framework.test import APITestCase

from main.models import StaffProfile


class BaseTest(APITestCase):

    fixtures = [
        'user.json',
        'goods.json',
        'hotel.json',
        "order.json",
        "integral.json",
        'room_style.json',
        'distribution_apply.json'
    ]

    def setUp(self):
        self.login_user = StaffProfile.objects.get(user=1)
        self.client.force_authenticate(user=self.login_user.user)
