# coding:utf-8
# Time    : 2018/10/7 下午10:24
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from django.db import transaction
from main.models import HotelOrderComment, CommentReply


class CreateReplySerializer(serializers.ModelSerializer):

    @transaction.atomic
    def create(self, validated_data):
        comment = validated_data.get("comment")
        if comment:
            comment.is_reply = True
            comment.save()
        instance = super(CreateReplySerializer, self).create(validated_data)

        return instance

    class Meta:
        model = CommentReply
        fields = (
            'id',
            'comment',
            'reply_content'
        )


class UpdateCommentDisplaySerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        comment_display = attrs.get("comment_show") or self.instance.comment_show
        no_show_reason = attrs.get('no_show_reason') or self.instance.no_show_reason
        if comment_display == 10 and not no_show_reason:
            raise serializers.ValidationError("评论对外不可见时,须要传递不显示原因")

        return attrs

    class Meta:
        model = HotelOrderComment
        fields = (
            'id',
            'comment_show',
            'no_show_reason'
        )


class ReplaySerializer(serializers.ModelSerializer):
    reply_staff_name = serializers.CharField(
        source='reply_staff.user_name',
        read_only=True
    )

    class Meta:
        model = CommentReply
        fields = (
            'id',
            'reply_staff',
            'reply_time',
            'reply_content',
            'reply_staff_name'
        )


class CommentSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField(
        source='commenter.user_name',
        read_only=True
    )
    comment_show_display = serializers.CharField(
        source='get_comment_show_display',
        read_only=True
    )
    comment_level_display = serializers.CharField(
        source='get_comment_level_display',
        read_only=True
    )
    belong_order_type_display = serializers.CharField(
        source='belong_order.get_order_type_display',
        read_only=True
    )
    belong_order_type = serializers.CharField(
        source='belong_order.order_type',
        read_only=True
    )

    comment_reply = ReplaySerializer()

    class Meta:
        model = HotelOrderComment
        fields = (
            'id',
            'belong_order',
            'comment_show',
            'belong_order_type',
            'belong_order_type_display',
            'comment_show_display',
            'commenter',
            'commenter_name',
            'content',
            'comment_level',
            'comment_level_display',
            'create_time',
            'is_reply',
            'comment_reply'
        )

