# coding:utf-8
from __future__ import unicode_literals

from django.db import models

from main.modelfields.JsonFields import JSONField


class Hotel(models.Model):
    name = models.CharField(
        '宾馆名称',
        max_length=100,
        unique=True,
        db_index=True
    )
    address = models.CharField(
        u'地址',
        max_length=100
    )
    longitude = models.CharField(
        '经度',
        max_length=100,
        blank=True,
        null=True
    )
    latitude = models.CharField(
        '纬度',
        max_length=100,
        blank=True,
        null=True

    )
    images = JSONField(
        '图片',
        default='[]',
        blank=True,
        null=True,
        help_text='图片，存放图片的URL'
    )
    hotel_profile = models.TextField(
        '宾馆简介'
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '宾馆信息'
        verbose_name_plural = verbose_name


class RoomStyles(models.Model):
    belong_hotel = models.ForeignKey(
        'main.Hotel',
        on_delete=models.SET_DEFAULT,
        verbose_name='所属酒店',
        default=0
    )
    style_name = models.CharField(
        '房间类型',
        max_length=100,
        db_index=True
    )
    price = models.DecimalField(
        '单价',
        max_digits=10,
        decimal_places=2,
    )
    room_profile = models.TextField(
        '详情'
    )
    images = JSONField(
        '图片列表',
        default='[]'
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    is_active = models.BooleanField(
        '是否对外销售',
        default=True,
        blank=True
    )

    def __unicode__(self):
        return self.style_name

    @property
    def left_room_count(self):
        return self.room.filter(room_status=10).count()

    @property
    def room_count(self):
        return self.room.count()

    class Meta:
        verbose_name = '房间类型'
        verbose_name_plural = verbose_name


class Rooms(models.Model):
    ROOM_STATUS = (
        (10, '未入住'),
        (20, '已预定'),
        (30, '入住'),
        (40, '退房'),
    )
    room_style = models.ForeignKey(
        'main.RoomStyles',
        on_delete=models.CASCADE,
        verbose_name='房间类型',
        related_name='room'
    )
    room_nums = models.CharField(
        '房间编号',
        max_length=20,
        db_index=True,
        unique=True
    )
    room_status = models.IntegerField(
        '房间状态',
        choices=ROOM_STATUS,
        default=10
    )
    reserve_time = models.DateTimeField(
        '预定时间',
        blank=True,
        null=True,
        help_text='预定时间'
    )

    reserve_out_time = models.DateTimeField(
        '预定结束时间',
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.room_nums

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = verbose_name
