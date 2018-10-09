# coding:utf-8
# Time    : 2018/10/9 下午10:57
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import HotelOrderComment, CommentReply
from main.apps.comment import serializers


class CommentViews(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    list:
        返回当前用户的所有评论
    retrieve:
        返回评论详情
    create:
        创建一个评论
    """
    queryset = HotelOrderComment.objects.all().prefetch_related('commentreply')
    serializer_class = serializers.CreateHotelOrderCommentSerializer

    def get_queryset(self):
        return self.queryset.filer(commenter=self.request.user.consumer)
