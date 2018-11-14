# coding:utf-8
# Time    : 2018/11/14 下午10:08
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import Opinions
from main.apps.admin_opinions import serializers


class AdminOpinionsViews(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Opinions.objects.all()
    serializer_class = serializers.OpinionsSerializers
