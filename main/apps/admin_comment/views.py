# coding:utf-8
# Time    : 2018/10/7 下午10:41
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from main.models import HotelOrderComment, CommentReply
from main.apps.admin_comment import serializers


class HotelOrderCommentViews(mixins.ListModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             viewsets.GenericViewSet):
    """
    create:
        创建回复评论
        ```
         COMMENT_DISPLAY = (
        (10, '评论人可见'),
        (20, '所有人可见')
        )
        ```
    update:
        更新评论的显示
    retrieve:
        评论详情
    list:
        返回所有用户评论
        ```
        COMMENT_DISPLAY = (
        (10, '评论人可见'),
        (20, '所有人可见')
        )

        COMMENT_LEVEL = (
        (10, '一分'),
        (20, '两分'),
        (30, '三分'),
        (40, '四分'),
        (50, '五分')
        )
        ```
    """

    queryset = HotelOrderComment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'staffprofile'):
            serializer.save(reply_staff=self.request.user.staffprofile)
        serializer.save()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateReplySerializer
        if self.action in ('update', 'partial_update'):
            return serializers.UpdateCommentDisplaySerializer
        return self.serializer_class

    def get_queryset(self):
        if self.action == 'create':
            return CommentReply.objects.all().prefetch_related('comment_reply')
        return self.queryset

