# coding:utf-8

from rest_framework import serializers

from main.models import GoodsCategory, Goods, HotelOrderComment, CommentReply
from main.common.seriliazer_fields import ImageField


class GoodsSerializer(serializers.ModelSerializer):
    goods_category = serializers.CharField(
        source='category.category_name',
        read_only=True
    )
    goods_integral = serializers.CharField(
        source='need_integral',
        read_only=True
    )
    images = ImageField()

    class Meta:
        model = Goods
        fields = (
            'id',
            "goods_name",
            'goods_price',
            'goods_category',
            'cover_image',
            'images',
            'need_integral',
            'is_integral',
            'goods_integral',
            'is_promotion',
            'is_special'
        )


class GoodsCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsCategory
        fields = (
            'id',
            'category_name',
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
