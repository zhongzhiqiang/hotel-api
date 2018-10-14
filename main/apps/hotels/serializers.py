# coding:utf-8

from rest_framework import serializers

from main.models import Hotel, RoomStyles, CommentReply, HotelOrderComment
from main.common.seriliazer_fields import ImageField, TagsField


class HotelSerializers(serializers.ModelSerializer):
    address = serializers.CharField(read_only=True)
    tags = TagsField()
    images = ImageField()

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
            'images'
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
            'tags'
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
            "comment_reply"
        )