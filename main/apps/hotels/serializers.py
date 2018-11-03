# coding:utf-8

import decimal
from rest_framework import serializers
from django.db.models import Avg, Q

from main.models import Hotel, RoomStyles, CommentReply, HotelOrderComment
from main.common.seriliazer_fields import ImageField, TagsField


class HotelSerializers(serializers.ModelSerializer):
    address = serializers.CharField(read_only=True)
    tags = TagsField()
    images = ImageField()

    comment_count = serializers.SerializerMethodField()
    avg_level = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        user = self.context['request'].user
        query_params = Q(comment_show=20)
        if hasattr(user, 'consumer'):
            query_params = query_params | Q(commenter=user.consumer)
        query_params = query_params & Q(belong_order__belong_hotel=obj)

        return HotelOrderComment.objects.filter(query_params).count()

    def get_avg_level(self, obj):
        user = self.context['request'].user
        query_params = Q(comment_show=20)
        if hasattr(user, 'consumer'):
            query_params = query_params | Q(commenter=user.consumer)
        query_params = query_params & Q(belong_order__belong_hotel=obj)
        level = HotelOrderComment.objects.filter(query_params).aggregate(level=Avg('comment_level')).get("level") or 0
        return str(0) if level == 0 else float('"%.1f" % level)')

    class Meta:
        model = Hotel
        fields = (
            'id',
            'name',
            'address',
            'province',
            'city',
            'area',
            'street',
            'longitude',
            'latitude',
            'cover_images',
            'hotel_profile',
            'min_price',
            'tel',
            'tags',
            'images',
            'comment_count',
            'avg_level'
        )


class RoomStyleSerializer(serializers.ModelSerializer):
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )
    images = ImageField()
    tags = TagsField()

    class Meta:
        model = RoomStyles
        fields = (
            'id',
            'belong_hotel_name',
            'belong_hotel',
            'room_count',
            'style_name',
            'price',
            'images',
            'room_profile',
            'cover_image',
            'tags',
        )


class HotelDetailSerializer(serializers.ModelSerializer):
    room_styles = RoomStyleSerializer(many=True)
    tags = TagsField()
    images = ImageField()

    comment_count = serializers.SerializerMethodField()
    avg_level = serializers.SerializerMethodField()

    def get_comment_count(self, obj):
        user = self.context['request'].user
        query_params = Q(comment_show=20)
        if hasattr(user, 'consumer'):
            query_params = query_params | Q(commenter=user.consumer)
        query_params = query_params & Q(belong_order__belong_hotel=obj)

        return HotelOrderComment.objects.filter(query_params).count()

    def get_avg_level(self, obj):
        user = self.context['request'].user
        query_params = Q(comment_show=20)
        if hasattr(user, 'consumer'):
            query_params = query_params | Q(commenter=user.consumer)
        query_params = query_params & Q(belong_order__belong_hotel=obj)

        level = HotelOrderComment.objects.filter(query_params).aggregate(level=Avg('comment_level')).get("level") or 0
        return str(0) if level == 0 else float('"%.1f" % level)')

    class Meta:
        model = Hotel
        fields = (
            'id',
            'name',
            'address',
            'province',
            'city',
            'area',
            'street',
            'longitude',
            'latitude',
            'cover_images',
            'hotel_profile',
            'min_price',
            'tel',
            'room_styles',
            'tags',
            'images',
            'comment_count',
            'avg_level'
        )


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = "__all__"


class HotelCommentSerializer(serializers.ModelSerializer):
    commenter_name = serializers.CharField(
        source='commenter.user_name',
        read_only=True
    )
    comment_level_display = serializers.CharField(
        source='get_comment_level_display',
        read_only=True,
    )
    comment_avatar_url = serializers.CharField(
        source='commenter.avatar_url',
        read_only=True
    )
    comment_reply = CommentReplySerializer()

    class Meta:
        model = HotelOrderComment
        fields = (
            "id",
            "commenter",
            "commenter_name",
            "comment_level",
            "content",
            'comment_level_display',
            "create_time",
            "comment_reply",
            'comment_avatar_url'
        )