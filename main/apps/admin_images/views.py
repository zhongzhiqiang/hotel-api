# coding:utf-8
# Time    : 2018/8/28 下午3:28
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import Images
from main.apps.admin_images import serializers


class ImageViews(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):

    def perform_create(self, serializer):
        if self.request.user and hasattr(self.request.user, 'staffprofile'):
            serializer.save(operator_name=self.request.user.staffprofile)
        serializer.save()

    queryset = Images.objects.all()
    serializer_class = serializers.ImageSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateImageSerializer
        return self.serializer_class
