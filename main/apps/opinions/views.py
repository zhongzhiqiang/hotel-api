# coding:utf-8
# Time    : 2018/11/14 下午10:12
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import viewsets

from main.apps.opinions import serializers
from main.models import Opinions


class OpinionsViews(viewsets.ModelViewSet):
    serializer_class = serializers.OpinionsSerializer
    queryset = Opinions.objects.all()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'consumer'):
            serializer.save(consumer=self.request.user.consumer)
