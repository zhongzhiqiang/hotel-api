# coding:utf-8
# Time    : 2018/10/30 下午9:07
# Author  : Zhongzq
# Site    : 
# File    : tests.py
# Software: PyCharm
from rest_framework.test import APITestCase
from django.urls import reverse

from main.models import StaffProfile, Banners


class BannerTest(APITestCase):

    fixtures = [
        'user.json'
    ]

    def setUp(self):
        self.login_user = StaffProfile.objects.get(user=1)
        self.client.force_authenticate(user=self.login_user.user)

    def test_post_user(self):
        url = '/admin/banner/'
        data = {
            "banner_title": "1234",
            "banner_images": "https://12345.com",
            "is_show": True
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Banners.objects.all().count(), 1)
