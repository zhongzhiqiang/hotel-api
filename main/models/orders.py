# coding:utf-8
from __future__ import unicode_literals

import datetime

from django.db import models

from main.common.defines import PayType, OrderStatus, OrderType


class Order(models.Model):
    ORDER_STATUS = (
        (OrderStatus.pre_pay, '未支付'),
        (OrderStatus.deliver, '待发货'),
        (OrderStatus.take_deliver, '待收货'),
        (OrderStatus.to_check_in, '待入住'),
        (OrderStatus.check_in, '入住中'),
        (OrderStatus.success, '待评价'),
        (OrderStatus.canceled, '已取消'),
        (OrderStatus.finish, '已评价'),
        (OrderStatus.prp_refund, '等待退款'),
        (OrderStatus.refund_ing, '退款中'),
        (OrderStatus.refunded, '退款完成'),
        (OrderStatus.pasted, '已过期'),
        (OrderStatus.deleted, '已删除')
    )
    PAY_TYPE = (
        (PayType.integral, '积分'),
        (PayType.balance, '余额'),
        (PayType.weixin, '微信支付')
    )
    ORDER_TYPE = (
        (OrderType.market, '商场订单'),
        (OrderType.hotel, '住宿订单'),
    )
    order_type = models.IntegerField(
        '订单类型',
        choices=ORDER_TYPE,
        db_index=True,
    )
    order_id = models.CharField(
        '订单号',
        max_length=30,
        db_index=True,
        blank=True,
        default='',
    )
    belong_hotel = models.ForeignKey(
        'main.Hotel',
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
        help_text='只有当订单类型为住宿时才会有此字段'
    )

    order_status = models.IntegerField(
        '订单状态',
        choices=ORDER_STATUS,
        default=10,
        blank=True,
        db_index=True
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    pay_type = models.IntegerField(
        '支付方式',
        choices=PAY_TYPE,
        default=PayType.weixin,
        db_index=True,
        help_text='默认微信支付'
    )
    pay_time = models.DateTimeField(
        '支付时间',
        blank=True,
        null=True
    )
    num = models.PositiveIntegerField(
        '总数',
        default=0,
        help_text='商品总数或者房间总数'
    )

    order_amount = models.DecimalField(
        '订单价格',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='需要支付的金额'
    )

    integral = models.PositiveIntegerField(
        '积分总额',
        default=0,
        help_text='只有当支付方式为积分时才会有这个字段'
    )
    consumer = models.ForeignKey(
        'main.Consumer',
        on_delete=models.SET_NULL,
        verbose_name='用户',
        null=True,
        blank=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        on_delete=models.SET_NULL,
        verbose_name='操作人员',
        null=True,
        blank=True
    )
    operator_time = models.DateTimeField(
        '操作时间',
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

    operator_remark = models.CharField(
        '操作人员备注',
        max_length=200,
        default=''
    )

    @property
    def image(self):
        # TODO 商场订单没有照片
        if self.order_type == OrderType.market:
            return self.market_order_detail.image
        else:
            return self.hotel_order_detail.image

    def make_order_id(self):
        """创建订单号"""
        return '%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    def __unicode__(self):
        return '%s, %s' % (self.get_order_type_display(), self.order_id)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class MarketOrderDetail(models.Model):
    market_order = models.OneToOneField(
        'main.Order',
        verbose_name='商场订单',
        related_name='market_order_detail',
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
    consignee_name = models.CharField(
        '收货人姓名',
        max_length=50,
        default=''
    )
    consignee_address = models.CharField(
        '收货地址',
        max_length=200,
        default=''
    )
    consignee_phone = models.CharField(
        '收货人电话',
        max_length=15,
        default=''
    )

    @property
    def order_goods_price(self):
        return self.sale_price * self.nums

    @property
    def goods_name(self):
        return self.goods.goods_name

    @property
    def image(self):
        return self.goods.cover_image

    @property
    def is_special(self):
        return self.goods.is_special

    @property
    def vip_info(self):
        if hasattr(self.goods, 'vip_info'):
            return self.goods.vip_info
        return None

    def __unicode__(self):
        if self.market_order:
            return '%s, %s' % (self.market_order.order_id, self.goods.goods_name)
        return '%s' % self.goods.goods_name

    class Meta:
        verbose_name = '商场订单明细'
        verbose_name_plural = verbose_name


class HotelOrderDetail(models.Model):
    hotel_order = models.OneToOneField(
        'main.Order',
        null=True,
        blank=True,
        related_name='hotel_order_detail',
        on_delete=models.SET_NULL,
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
        max_digits=10,
        decimal_places=2,
    )

    reserve_check_in_time = models.DateTimeField(
        '预定入住时间',
        help_text='用户预定时间，12点以后',
        null=True,
    )
    reserve_check_out_time = models.DateTimeField(
        '预定退房时间',
        help_text='用户预定时间',
        null=True
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
    def room_style_name(self):
        return self.room_style.style_name

    @property
    def image(self):
        return self.room_style.cover_image

    @property
    def days(self):
        return (self.reserve_check_out_time - self.reserve_check_in_time).days

    def __unicode__(self):
        return self.room_style_name

    class Meta:
        verbose_name = '住宿订单详情'
        verbose_name_plural = verbose_name


class OrderPay(models.Model):
    order = models.OneToOneField(
        'main.Order',
        verbose_name='订单支付信息',
        related_name='order_pay',
        null=True,
        on_delete=models.SET_NULL
    )
    wx_order_id = models.CharField(
        '微信支付订单号',
        max_length=32,
        blank=True,
        null=True,
        default=0
    )
    free_money = models.DecimalField(
        '免费金额',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    integral = models.PositiveIntegerField(
        '支付积分',
        default=0
    )

    money = models.DecimalField(
        '金额',
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='非免费金额,微信支付为实际金额, 余额支付为从充值金额扣去部分'
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )

    def __unicode__(self):
        return 'pay info %s' % self.order.order_id

    class Meta:
        verbose_name = '支付信息'
        verbose_name_plural = verbose_name


class OrderRefunded(models.Model):
    order = models.OneToOneField(
        'main.Order',
        verbose_name='关联订单',
        related_name='order_refunded',
        on_delete=models.SET_NULL,
        null=True,
    )

    refunded_order_id = models.CharField(
        '退款订单号',
        max_length=30,
        default=''
    )

    refunded_money = models.DecimalField(
        '退款金额',
        help_text='微信支付时,此金额为用户微信支付金额,余额支付时为充值金额',
        default=0,
        max_digits=10,
        decimal_places=2
    )
    refunded_free_money = models.DecimalField(
        '退款赠送金额',
        decimal_places=2,
        max_digits=10,
        default=0
    )
    refunded_integral = models.PositiveIntegerField(
        '退款积分',
        default=0
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )

    class Meta:
        verbose_name = '退款信息'
        verbose_name_plural = verbose_name
