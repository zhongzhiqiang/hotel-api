# coding:utf-8
# Time    : 2018/9/10 下午5:41
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.apps.admin_user import serializers
from main.models import StaffProfile


class AdminUserViews(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    create:
        创建后端管理员
    """
    queryset = StaffProfile.objects.all()
    serializer_class = serializers.StaffProfileSerializer

    def get_queryset(self):
        if self.request.user and self.request.user.is_superuser:
            return self.queryset
        else:
            if self.request.user and self.request.user.staffprofile:
                return self.queryset.filter(belong_hotel=self.request.user.staffprofile.belong_hotel)

        return self.request

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateStaffProfileSerializer
        return self.serializer_class

    # def perform_create(self, serializer):
    #     if self.request.user.is_superuser:
    #         belong_hotel = self.request.user.staffprofile.belong_hotel
    #         serializer.save(belong_hotel=belong_hotel)
    #     else:
    #         belong_hotel = self.request.user.staffprofile.belong_hotel
    #         serializer.save(belong_hotel=belong_hotel)
