# coding:utf-8

from rest_framework import serializers

from main.models import Hotel, RoomStyles, CommentReply, HotelOrderComment


class ImageField(serializers.CharField):
    def to_representation(self, value):
        if isinstance(value, basestring):
            return eval(value)
        return value


class TagsField(serializers.CharField):
    def to_representation(self, value):
        if isinstance(value, basestring):
            return eval(value)
        return value


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
    tags = serializers.CharField(read_only=True)

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
            'vip_price'
        )


class HotelDetailSerializer(serializers.ModelSerializer):
    room_styles = RoomStyleSerializer(many=True)

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