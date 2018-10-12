# coding:utf-8
# Time    : 2018/10/7 下午10:54
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers

from main.models import HotelOrderComment, CommentReply
from main.common.defines import OrderStatus


class CreateHotelOrderCommentSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        consumer = self.context['request'].user.consumer
        belong_order = attrs.get("belong_order")
        if belong_order.order_status != OrderStatus.success:
            raise serializers.ValidationError("当前订单暂时无法评论")

        if belong_order.consumer != consumer:
            raise serializers.ValidationError("无法评论其他用户订单")
        return attrs

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
