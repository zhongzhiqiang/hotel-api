# coding:utf-8
# Time    : 2018/10/7 下午10:15
# Author  : Zhongzq
# Site    : 
# File    : comment.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db import models


class HotelOrderComment(models.Model):

    COMMENT_DISPLAY = (
        (10, '评论人可见'),
        (20, '审核通过')
    )

    COMMENT_LEVEL = (
        (1, '一分'),
        (2, '两分'),
        (3, '三分'),
        (4, '四分'),
        (5, '五分')
    )
    belong_order = models.ForeignKey(
        'main.Order',
        verbose_name='关联订单',
    )
    goods = models.ForeignKey(
        'main.Goods',
        null=True,
        blank=True
    )

    comment_show = models.IntegerField(
        '评论可见',
        choices=COMMENT_DISPLAY,
        default=10,
        help_text='默认只能够评论人可见'
    )

    commenter = models.ForeignKey(
        'main.Consumer',
        verbose_name='评论人',
        null=True,
        blank=True
    )

    content = models.CharField(
        '评论内容',
        max_length=200,
        default='',
    )

    comment_level = models.IntegerField(
        '评论等级',
        choices=COMMENT_LEVEL,
        default=5
    )

    create_time = models.DateTimeField(
        '评论时间',
        auto_now_add=True
    )
    no_show_reason = models.CharField(
        '不显示原因',
        max_length=200,
        null=True,
        blank=True,
        default=''
    )
    is_reply = models.BooleanField(
        '是否回复',
        default=False,
        blank=True
    )

    def __unicode__(self):
        return "%s, %s" % (self.belong_order.id, self.comment_level)

    class Meta:
        verbose_name = '订单评论'
        verbose_name_plural = verbose_name


class CommentReply(models.Model):
    comment = models.OneToOneField(
        'main.HotelOrderComment',
        related_name='comment_reply'
    )

    reply_staff = models.ForeignKey(
        'main.StaffProfile',
        verbose_name='回复人',
        null=True,
        blank=True
    )
    reply_time = models.DateTimeField(
        '回复时间',
        auto_now_add=True
    )
    reply_content = models.CharField(
        '回复内容',
        max_length=200
    )

    class Meta:
        verbose_name = '评论回复'
        verbose_name_plural = verbose_name
