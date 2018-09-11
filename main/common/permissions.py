# coding:utf-8
# Time    : 2018/9/11 下午9:43
# Author  : Zhongzq
# Site    : 
# File    : permissions.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework.permissions import  BasePermission


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'consumer')
