# coding:utf-8
# Time    : 2018/9/10 下午9:00
# Author  : Zhongzq
# Site    : 
# File    : return_payload.py
# Software: PyCharm
from __future__ import unicode_literals


def jwt_response_payload_handler(token, user=None, request=None):
    kwargs = {
        "token": token
    }
    if user:
        kwargs.update({"username": user.username})

    if user and user.staffprofile:
        kwargs.update({"user_name": user.staffprofile.user_name})

    return kwargs
