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
        (1, '一星'),
        (2, '两星'),
        (3, '三星'),
        (4, '四星'),
        (5, '五星')
        ```
        {
        "belong_order": "string"  # 对应订单的ID。最外层ID
        comment_list: [{
        "goods": "商品ID，只有当商场订单才专递", 
            "content": "string",
            "comment_level": "string",
            }]
        }
        ```
    )
    """
    queryset = HotelOrderComment.objects.all().prefetch_related('comment_reply')
    serializer_class = serializers.HotelOrderCommentSerializer

    def perform_create(self, serializer):
        serializer.save(commenter=self.request.user.consumer)

    def get_queryset(self):
        # 返回当前用户的所有评论以及回复。
        return self.queryset.filter(commenter=self.request.user.consumer)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateCommentSerializer
        return self.serializer_class
