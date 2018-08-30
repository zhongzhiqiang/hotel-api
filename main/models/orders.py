# coding:utf-8
from __future__ import unicode_literals

import datetime

from django.db import models

from main.modelfields.JsonFields import JSONField


class MarketOrder(models.Model):
    ORDER_STATUS = (
        (10, '未支付'),
        (20, '待发货'),
        (30, '待收货'),
        (40, '已完成'),
        (50, '已取消'),
    )

    order_id = models.CharField(
        '订单号',
        max_length=20,
        blank=True,
    )
    order_statue = models.IntegerField(
        '订单状态',
        choices=ORDER_STATUS,
        default=10,
        blank=True
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    pay_time = models.DateTimeField(
        '支付时间',
        blank=True,
        null=True
    )
    operator_time = models.DateTimeField(
        '操作时间',
        blank=True,
        null=True
    )
    user_remark = models.CharField(
        '用户备注',
        max_length=100,
        blank=True,
        null=True,
        default=''
    )
    operator_remark = models.CharField(
        '操作人员备注',
        max_length=100,
        blank=True,
        default='',
        null=True,
    )

    @property
    def goods_count(self):
        # 返回订单商品数量
        return self.market_order.count()

    def __unicode__(self):
        return self.order_id

    def make_order_id(self):
        """创建订单号"""
        return '%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    class Meta:
        verbose_name = '商场订单'
        verbose_name_plural = verbose_name


class MarketOrderDetail(models.Model):
    market_order = models.ForeignKey(
        'main.MarketOrder',
        verbose_name='商场订单',
        related_name='market_order',
        on_delete=models.CASCADE
    )

    goods = models.ForeignKey(
        'main.Goods',
        verbose_name='商品分类',
        related_name='goods',
    )
    sale_price = models.DecimalField(
        '销售单价',
        max_digits=5,
        decimal_places=2,
    )
    nums = models.PositiveIntegerField(
        '购买数量',
        default=0,
    )

    def __unicode__(self):
        return '%s, %s' % (self.market_order.order_id, self.goods.goods_name)

    class Meta:
        verbose_name = '商场订单明细'
        verbose_name_plural = verbose_name


class HotelOrder(models.Model):
    ORDER_STATUS = (
        (10, '待支付'),
        (20, '待入住'),
        (30, '入住中'),
        (40, '完成'),
        (50, '待评价'),
        (60, '取消'),
        (70, '待退款'),
        (80, '已退款')
    )
    belong_hotel = models.ForeignKey(
        'main.Hotel',
        on_delete=models.SET_DEFAULT,
        verbose_name='所属宾馆',
        null=True,
        default=0,
    )
    order_id = models.CharField(
        '订单号',
        max_length=20,
        blank=True,
        null=True
    )
    order_status = models.IntegerField(
        '订单状态',
        choices=ORDER_STATUS,
        default=10,
        blank=True
    )
    room_style_num = models.PositiveIntegerField(
        '房间类型数量',
        default=0,
        help_text='用于'
    )
    sale_price = models.DecimalField(
        '订单金额',
        max_digits=10,
        decimal_places=2,
    )
    reserve_check_in_time = models.DateTimeField(
        '预定入住时间',
        help_text='用户预定时间，12点以后'
    )
    reserve_check_out_time = models.DateTimeField(
        '预定退房时间',
        help_text='用户预定时间'
    )

    pay_time = models.DateTimeField(
        '支付时间',
        null=True,
        blank=True,
    )

    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    operator_time = models.DateTimeField(
        '操作时间',
        auto_now=True,
        blank=True
    )
    consumer = models.ForeignKey(
        'main.Consumer',
        on_delete=models.SET_NULL,
        verbose_name='用户',
        null=True
    )
    user_remark = models.TextField(
        '用户备注',
        default='',
        blank=True,
    )

    flow_remark = models.TextField(
        '跟进备注',
        default='',
        blank=True,
        help_text='管理人员备注'
    )

    def __unicode__(self):
        return self.order_id

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class HotelOrderDetail(models.Model):
    belong_order = models.ForeignKey(
        'main.HotelOrder',
        on_delete=models.CASCADE,
        verbose_name='所属订单',
        related_name='hotel_order_detail'
    )
    room_style = models.ForeignKey(
        'main.RoomStyles',
        verbose_name='房间类型',
        on_delete=models.SET_NULL,
        null=True
    )
    room_nums = models.PositiveIntegerField(
        '房间数量',
        default=0,
    )
    room_price = models.DecimalField(
        '入住时房间单价',
        max_digits=10,
        decimal_places=2,
    )

    def __unicode__(self):
        return self.room_style.style_name

    class Meta:
        verbose_name = '订单房间详情'
        verbose_name_plural = verbose_name


class HotelOrderRoomInfo(models.Model):

    belong_order = models.ForeignKey(
        'main.HotelOrder',
        on_delete=models.CASCADE,
        verbose_name='订单号',
        related_name='hotel_order_room_info'
    )
    check_in_room = models.ForeignKey(
        'main.Rooms',
        verbose_name='入住房间',
        help_text='这里入住时,需要把关联房间状态更改为入住',
        on_delete=models.SET_NULL,
        null=True
    )
    check_in_time = models.DateTimeField(
        '用户入住时间',
        blank=True,
        null=True
    )
    check_out_time = models.DateTimeField(
        '退房时间',
        blank=True,
        null=True
    )
    guest_nums = models.PositiveIntegerField(
        '入住人数',
        default=0,
        blank=True
    )
    # guest_info = [{"username":"","idcard_num": ""#加密},{"username":"","idcard_num": ""#加密},]
    guest_info = JSONField(
        '用户信息',
        default='[]',
        help_text='多个用户信息放入。存入数据库为string'
    )

    def __unicode__(self):
        return self.check_in_room.room_nums

    class Meta:
        verbose_name = '入住信息'
        verbose_name_plural = verbose_name
