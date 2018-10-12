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
        
        COMMENT_LEVEL = (
        (10, '一星'),
        (20, '两星'),
        (30, '三星'),
        (40, '四星'),
        (50, '五星')
        ```
        {
            "content": "string",
            "comment_level": "string",
            "belong_order": "string"  # 对应订单的ID。最外层ID
        }
        ```
    )
    """
    queryset = HotelOrderComment.objects.all().prefetch_related('commentreply')
    serializer_class = serializers.CreateHotelOrderCommentSerializer

    def perform_create(self, serializer):
        serializer.save(consumer=self.request.user.consumer)

    def get_queryset(self):
        # 返回当前用户的所有评论以及回复。
        return self.queryset.filer(commenter=self.request.user.consumer)
