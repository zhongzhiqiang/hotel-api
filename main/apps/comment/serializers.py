# coding:utf-8
# Time    : 2018/10/7 下午10:54
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import HotelOrderComment, CommentReply


class CreateHotelOrderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrderComment
        fields = (
            'id',
            'belong_order',
            'content',
            'comment_level',
            'create_time',
            'commenter'
        )
        read_only_fields = ('commenter', )


class CommentReplySerializer(serializers.ModelSerializer):
    reply_staff_name = serializers.CharField(
        source='reply_staff.user_name',
        read_only=True
    )

    class Meta:
        model = CommentReply
        fields = (
            'id',
            'reply_staff',
            'reply_staff_name',
            'reply_time',
            'reply_content'
        )


class HotelOrderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrderComment
        fields = (
            'id',
            'belong_order',
            'content',
            'comment_level',
            'create_time',
            'commenter'
        )