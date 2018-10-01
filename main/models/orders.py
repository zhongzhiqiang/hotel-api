# coding:utf-8
from __future__ import unicode_literals

import datetime

from django.db import models

from main.modelfields.JsonFields import JSONField
from main.common.defines import PayType


class MarketOrder(models.Model):
    ORDER_STATUS = (
        (10, '未支付'),
        (20, '待发货'),
        (30, '待收货'),
        (40, '已完成'),
        (50, '已取消'),
        (60, '等待评价'),
        (70, '评价完成')  # 评价完成后才有积分
    )
    PAY_TYPE = (
        (PayType.integral, '积分'),
        (PayType.balance, '余额'),
        (PayType.weixin, '微信支付')
    )

    order_id = models.CharField(
        '订单号',
        max_length=20,
        blank=True,
        default='',
    )
    order_status = models.IntegerField(
        '订单状态',
        choices=ORDER_STATUS,
        default=10,
        blank=True
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    pay_type = models.IntegerField(
        '支付方式',
        choices=PAY_TYPE,
        default=PayType.weixin,
        help_text='默认微信支付'
    )
    pay_money = models.DecimalField(
        '支付金额',
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0
    )
    pay_integral = models.PositiveIntegerField(
        '消费积分',
        default=0,
        help_text='当支付方式为积分时'
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
    consumer = models.ForeignKey(
        'main.Consumer',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    consignee_name = models.CharField(
        '收货人姓名',
        max_length=50,
        default=''
    )
    consignee_address = models.CharField(
        '收货人地址',
        max_length=200,
        default=''
    )
    consignee_phone = models.CharField(
        '收货人电话',
        max_length=15,
        default=''
    )

    @property
    def goods_count(self):
        # 返回订单商品数量
        return self.marketorderdetail.nums

    def __unicode__(self):
        return self.order_id

    def make_order_id(self):
        """创建订单号"""
        return 'market%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    class Meta:
        verbose_name = '商场订单'
        verbose_name_plural = verbose_name


class MarketOrderDetail(models.Model):
    market_order = models.OneToOneField(
        'main.MarketOrder',
        verbose_name='商场订单',

        blank=True,
        null=True,
    )
    goods = models.ForeignKey(
        'main.Goods',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    sale_price = models.DecimalField(
        '销售单价',
        max_digits=5,
        decimal_places=2,
        blank=True,
        default=0
    )
    integral = models.PositiveIntegerField(
        '兑换积分单价',
        blank=True,
        default=0,
    )
    nums = models.PositiveIntegerField(
        '购买数量',
        default=0,
    )

    @property
    def order_goods_price(self):
        return self.sale_price * self.nums

    def __unicode__(self):
        if self.market_order:
            return '%s, %s' % (self.market_order.order_id, self.goods.goods_name)
        return '%s' % self.goods.goods_name

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
    PAYTYPE = (
        (PayType.balance, '余额'),
        (PayType.weixin, '微信支付')
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
    pay_type = models.IntegerField(
        '支付类型',
        choices=PAYTYPE,
        default=PayType.weixin,
        help_text='默认微信支付'
    )
    room_style_num = models.PositiveIntegerField(
        '房间类型数量',
        default=0,
        help_text='用于统计订单有多少房间',
        blank=True,
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
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    consumer = models.ForeignKey(
        'main.Consumer',
        on_delete=models.SET_NULL,
        verbose_name='用户',
        null=True,
        blank=True
    )
    refund_reason = models.CharField(
        '退款原因',
        blank=True,
        max_length=200,
        default='',
        help_text='退款时,必须填写'
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
    contact_name = models.CharField(
        '联系人',
        max_length=50,
        default=''
    )
    contact_phone = models.CharField(
        '联系电话',
        max_length=20,
        default=''
    )

    @property
    def days(self):
        return (self.reserve_check_out_time - self.reserve_check_in_time).days

    def make_order_id(self):
        """创建订单号"""
        return 'hotel%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    def __unicode__(self):
        return self.order_id

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class HotelOrderDetail(models.Model):
    belong_order = models.OneToOneField(
        'main.HotelOrder',
        on_delete=models.CASCADE,
        verbose_name='所属订单',
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
        max_digits=5,
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
