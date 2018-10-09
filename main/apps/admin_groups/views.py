# coding:utf-8
# Time    : 2018/9/9 下午7:17
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from main.apps.admin_groups import serializers
from main.common.perms import permission


class RoleViews(mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """
    create:
        创建角色
        ```
        perms: 传递['codename']
        name: 角色名称
    update:
        更新角色
    list:
        返回所有的角色信息
    retrieve:
        返回角色的详细信息
    """
    queryset = Group.objects.all().prefetch_related('permissions', 'user_set')
    serializer_class = serializers.CreateRoleSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.RoleSerializer
        return self.serializer_class


class RolePermsConfig(APIView):

    def get(self, request, *args, **kwargs):
        """
        返回所有权限
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        return Response(permission)
