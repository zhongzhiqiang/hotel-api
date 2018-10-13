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
    province = models.CharField(
        '省份',
        max_length=100,
        default='四川省',
    )
    city = models.CharField(
        '市',
        max_length=20,
        default='成都市'
    )
    area = models.CharField(
        '区',
        max_length=100,
        default=''
    )
    street = models.CharField(
        '街道地址',
        max_length=200,
        default=''
    )
    longitude = models.CharField(
        '经度',
        max_length=100,
        default=''
    )
    latitude = models.CharField(
        '纬度',
        max_length=100,
        default=''
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
    cover_images = models.CharField(
        '封面图',
        max_length=100,
        default=''
    )
    tel = models.CharField(
        '联系电话',
        max_length=50,
        default=''
    )
    tags = JSONField(
        '标签管理',
        default=[],
        blank=True,
        help_text='标签,存放为数组,数据库为json后的list'
    )
    is_active = models.BooleanField(
        '是否对外开放',
        default=False,
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='操作人员'
    )

    def __unicode__(self):
        return self.name

    @property
    def min_price(self):
        return self.room_styles.aggregate(min_price=models.Min('price')).get('min_price') or '0'

    @property
    def address(self):
        return self.province + self.city + self.area + self.street

    class Meta:
        verbose_name = '宾馆信息'
        verbose_name_plural = verbose_name


class RoomStyles(models.Model):
    belong_hotel = models.ForeignKey(
        'main.Hotel',
        on_delete=models.SET_DEFAULT,
        verbose_name='所属酒店',
        related_name='room_styles',
        default=0
    )
    style_name = models.CharField(
        '房间类型',
        max_length=100,
        db_index=True,
        unique=True,
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
        default=[],
        blank=True,
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    cover_image = models.CharField(
        '封面图',
        default='',
        max_length=100,
    )
    room_count = models.PositiveIntegerField(
        '房间数',
        default=0,
    )
    is_active = models.BooleanField(
        '是否对外销售',
        default=True,
        blank=True
    )
    # is_promotion = models.BooleanField(
    #     '是否促销',
    #     default=False,
    #     blank=True
    # )
    # promotion_price = models.DecimalField(
    #     '促销价格',
    #     decimal_places=2,
    #     max_digits=10,
    #     default=0
    # )
    # promotion_start = models.DateTimeField(
    #     '促销开始时间',
    #     blank=True,
    #     null=True
    # )
    # promotion_end = models.DateTimeField(
    #     '促销结束时间',
    #     blank=True,
    #     null=True
    # )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    @property
    def vip_price(self):
        from decimal import Decimal
        return self.price * Decimal(0.8)

    def __unicode__(self):
        return self.style_name

    class Meta:
        verbose_name = '房间类型'
        verbose_name_plural = verbose_name


class Rooms(models.Model):
    ROOM_STATUS = (
        (10, '未入住'),
        (20, '已预定'),
        (30, '入住'),
        (40, '退房'),
        (50, '维修'),
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
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now_add=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __unicode__(self):
        return self.room_nums

    class Meta:
        verbose_name = '房间'
        verbose_name_plural = verbose_name
