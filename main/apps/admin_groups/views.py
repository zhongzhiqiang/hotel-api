# coding:utf-8
# Time    : 2018/9/9 下午7:17
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from rest_framework import mixins, viewsets

from main.apps.admin_groups import serializers


class GroupsViews(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    create:
        创建角色
    update:
        更新角色
    list:
        返回所有的角色信息
    retrieve:
        返回角色的详细信息
    """
    queryset = Group.objects.all()
    serializer_class = serializers.CreateRoleSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RoleSerializer
        return self.serializer_class

