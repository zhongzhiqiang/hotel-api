# coding:utf-8
# Time    : 2018/10/7 下午10:54
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from django.db import transaction

from main.models import HotelOrderComment, CommentReply
from main.common.defines import OrderStatus


class CreateHotelOrderCommentSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField(
        source='commenter.user_name',
        read_only=True
    )

    def validate(self, attrs):
        consumer = self.context['request'].user.consumer
        belong_order = attrs.get("belong_order")
        if belong_order.order_status != OrderStatus.success:
            raise serializers.ValidationError("当前订单暂时无法评论")

        if belong_order.consumer != consumer:
            raise serializers.ValidationError("无法评论其他用户订单")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        instance = super(CreateHotelOrderCommentSerializer, self).create(validated_data)
        instance.belong_order.order_status = OrderStatus.finish
        instance.belong_order.save()
        return instance

    class Meta:
        model = HotelOrderComment
        fields = (
            'id',
            'belong_order',
            'content',
            'comment_level',
            'create_time',
            'commenter',
            'commenter_name'
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
    comment_avatar_url = serializers.CharField(
        source='commenter.avatar_url',
        read_only=True
    )
    comment_reply = CommentReplySerializer(read_only=True)

    class Meta:
        model = HotelOrderComment
        fields = (
            'id',
            'belong_order',
            'content',
            'comment_level',
            'create_time',
            'commenter'
            'comment_avatar_url',
            'comment_reply'
        )
