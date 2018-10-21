# coding:utf-8
# Time    : 2018/9/11 下午9:43
# Author  : Zhongzq
# Site    : 
# File    : permissions.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'consumer')


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'staffprofile')


class PermsRequired(BasePermission):

    def __init__(self, *perms):
        self.perms = perms

    def __call__(self):
        return self

    def has_permission(self, request, view):
        user = request.user

        if user.is_superuser:
            return True
        user_perms = user.get_all_permissions()
        return True if user_perms & set(self.perms) else False