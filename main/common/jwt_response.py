# coding:utf-8
# Time    : 2018/9/10 下午9:00
# Author  : Zhongzq
# Site    : 
# File    : return_payload.py
# Software: PyCharm
from __future__ import unicode_literals


def get_user_perms(user):
    all_perms = user.get_all_permissions()
    user_perms = [
        perm.split('.')[1]
        for perm in all_perms if perm.split('.')[0] == 'main' and not perm.split('.')[1].startswith(('add', 'delete', 'change'))
    ]
    return user_perms


def jwt_response_payload_handler(token, user=None, request=None):
    kwargs = {
        "token": token,
        "perms": get_user_perms(user),
    }
    if user:
        kwargs.update({"username": user.username})

    if user and hasattr(user, 'consumer'):
        kwargs.update({"user_id": user.consumer.id})
        kwargs.update({"sell_user": user.consumer.sell_user_id or ''})

    if user and hasattr(user, 'staffprofile'):
        kwargs.update({"user_name": user.staffprofile.user_name})

    return kwargs
