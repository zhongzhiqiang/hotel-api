# coding:utf-8
# Time    : 2018/10/7 下午10:54
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

from rest_framework import serializers
from django.db import transaction

from main.models import HotelOrderComment, CommentReply, Order, Goods
from main.common.defines import OrderStatus, OrderType


class CommentSerializer(serializers.Serializer):
    goods = serializers.PrimaryKeyRelatedField(
        required=False,
        queryset=Goods.objects.all(),
        allow_empty=True,
        allow_null=True,
        write_only=True
    )
    content = serializers.CharField(max_length=200)
    comment_level = serializers.ChoiceField(choices=(1, 2, 3, 4, 5, '1', '2', '3', '4', '5'))


class CreateCommentSerializer(serializers.Serializer):
    belong_order = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Order.objects.all()
    )
    comment_list = CommentSerializer(many=True)

    def validate(self, attrs):
        belong_order = attrs['belong_order']
        comment_list = attrs['comment_list']
        if belong_order.order_status not in (OrderStatus.success, OrderStatus.finish):
            raise serializers.ValidationError("当前订单未完成无法评论")

        if belong_order.order_type == OrderType.market:
            if belong_order.market_order_detail.count() != len(comment_list):
                raise serializers.ValidationError("请评价完所有商品")
            for comment in comment_list:
                if not comment.get("goods"):
                    raise serializers.ValidationError("请传递商品ID")
                order = belong_order.market_order_detail.filter(goods=comment['goods']).first()
                is_comment = HotelOrderComment.objects.filter(belong_order=belong_order, goods=comment['goods']).first()
                if is_comment:
                    remark = u'{}:商品已评论'.format(comment['goods'].goods_name)
                    raise serializers.ValidationError(remark)
                if not order:
                    raise serializers.ValidationError("无法评论非当前订单商品")

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        consumer = self.context['request'].user.consumer
        comment_list = validated_data['comment_list']
        for comment in comment_list:
            comment.update({"commenter": consumer, "belong_order": validated_data['belong_order']})
            HotelOrderComment.objects.create(**comment)

        validated_data['belong_order'].order_status = OrderStatus.finish
        validated_data['belong_order'].save()

        return validated_data


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
            'commenter',
            'comment_avatar_url',
            'comment_reply'
        )
