# coding:utf-8
from __future__ import unicode_literals

import uuid
import datetime

from django.db import models

from main.common.defines import PayType, OrderStatus, OrderType, RefundedStatus
from main.modelfields.JsonFields import JSONField


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
        (OrderStatus.apply_refund, '申请退款'),
        (OrderStatus.fill_apply, '请退货'),
        (OrderStatus.pre_refund, '等待退款'),
        (OrderStatus.refund_ing, '退款中'),
        (OrderStatus.refunded, '退款完成'),
        (OrderStatus.refunded_fail, '退款拒绝'),
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
        blank=True,
        null=True,
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
        default='',
        blank=True
    )

    fail_reason = models.CharField(
        '退款失败原因',
        max_length=100,
        default='',
        blank=True,
    )

    @property
    def image(self):
        # TODO 商场订单没有照片
        if self.order_type == OrderType.market:
            return self.market_order_detail.all().values_list('goods__images', flat=True)
        else:
            return self.hotel_order_detail.image

    @property
    def goods_names(self):
        return self.market_order_detail.all().values_list('goods.goods_name', flat=True)

    def make_order_id(self):
        """创建订单号"""
        return '%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    def __unicode__(self):
        return '%s, %s' % (self.get_order_type_display(), self.order_id)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class MarketOrderDetail(models.Model):
    # 商场订单详细与商品为一对多关系
    market_order = models.ForeignKey(
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
    goods_price = models.DecimalField(
        '销售单价',
        max_digits=5,
        decimal_places=2,
        blank=True,
        default=0
    )

    goods_integral = models.PositiveIntegerField(
        '兑换积分单价',
        blank=True,
        default=0,
        null=True
    )

    nums = models.PositiveIntegerField(
        '购买数量',
        default=0,
    )

    @property
    def single_goods_amount(self):
        return self.goods_price * self.nums

    @property
    def goods_name(self):
        return self.goods.goods_name

    @property
    def cover_image(self):
        return self.goods.cover_image

    @property
    def is_special(self):
        return self.goods.is_special

    @property
    def vip_info(self):
        if hasattr(self.goods, 'vip_info'):
            return self.goods.vip_info
        return None

    @property
    def is_integral(self):
        return self.goods.is_integral

    def __unicode__(self):
        if self.market_order:
            return '%s, %s' % (self.market_order.order_id, self.goods.goods_name)
        return '%s' % self.goods.goods_name

    class Meta:
        verbose_name = '商场订单明细'
        verbose_name_plural = verbose_name


class MarketOrderContact(models.Model):
    # 商场订单的收货人
    order = models.OneToOneField(
        'main.Order',
        blank=True,
        null=True,
        related_name='market_order_contact'
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

    def __unicode__(self):
        return "%s, %s" % (self.order.order_id, self.consignee_name)

    class Meta:
        verbose_name = '商场订单收货人'
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
        default=0,
        blank=True,
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

    WX_REFUND_STATUS = (
        (RefundedStatus.refunded_ing, '退款中'),
        (RefundedStatus.success, '成功'),
        (RefundedStatus.fail, '失败'),
        (RefundedStatus.retry, '重试'),
        (RefundedStatus.unknown, '未知')
    )

    order = models.OneToOneField(
        'main.Order',
        verbose_name='关联订单',
        related_name='order_refunded',
        on_delete=models.SET_NULL,
        null=True,
    )
    refunded_status = models.IntegerField(
        "退款状态",
        default=RefundedStatus.unknown,
        help_text='退款状态。微信可能会退款失败',
        choices=WX_REFUND_STATUS,
    )
    refunded_message = models.CharField(
        "退款描述",
        default='',
        blank=True,
        max_length=100
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
    refunded_account = models.DateTimeField(
        '退款到账时间',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.refunded_order_id

    @classmethod
    def make_order_id(cls):
        """创建订单号"""
        order_time = datetime.datetime.now().strftime("%Y%m%d")
        return_order_id = uuid.uuid1().get_hex().upper()[:24]
        return order_time + return_order_id

    class Meta:
        verbose_name = '退款信息'
        verbose_name_plural = verbose_name


class Cart(models.Model):

    consumer = models.ForeignKey(
        "main.Consumer",
        null=True,
        blank=True
    )
    goods = models.ForeignKey(
        "main.Goods",
        verbose_name='商品'
    )

    nums = models.PositiveIntegerField(
        "商品数量",
        default=0
    )

    def __unicode__(self):
        return "购物车-{}, {}".format(self.consumer, self.goods)

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


class MarketOrderExpress(models.Model):
    order = models.OneToOneField(
        'main.Order',
        related_name='order_express',
        verbose_name='订单'
    )
    express_id = models.CharField(
        '快递单号',
        max_length=100,
    )
    express_name = models.CharField(
        '快递名称',
        max_length=100
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )

    class Meta:
        verbose_name = '订单快递信息'
        verbose_name_plural = verbose_name


class WeiXinPayInfo(models.Model):
    order = models.ForeignKey(
        "main.Order",
        blank=True,
        null=True,
    )

    wx_order_id = models.CharField(
        "传递给订单号",
        blank=True,
        max_length=30,
        default='',
        help_text='随机生成'
    )
    create_time = models.DateTimeField(
        "创建时间",
        auto_now_add=True
    )
    call_back_result = models.CharField(
        "回调结果",
        default='',
        blank=True,
        max_length=20
    )
    call_back_result_code = models.CharField(
        "回调业务结果",
        default='',
        blank=True,
        max_length=20
    )
    call_return_msg = models.CharField(
        '回调描述',
        default='',
        blank=True,
        max_length=100
    )

    def make_order_id(self):
        """创建订单号"""
        return 'wx%s%8.8d' % (datetime.date.today().strftime('%Y%m%d'), self.id)

    def __unicode__(self):
        return self.wx_order_id

    class Meta:
        verbose_name = '微信支付信息'
        verbose_name_plural = verbose_name


class AdminRefundedInfo(models.Model):
    order = models.OneToOneField(
        'main.Order',
        null=True,
        blank=True,
        verbose_name='退款地址',
        related_name='admin_refunded_info'
    )
    refunded_address = models.CharField(
        '退款收货地址',
        max_length=200,
        default='',
        blank=True,
    )
    refunded_name = models.CharField(
        '退款收货人',
        max_length=200,
        default='',
        blank=True,
    )
    refunded_phone = models.CharField(
        '退款联系电话',
        max_length=30,
        default='',
        blank=True
    )
    remark = models.CharField(
        '备注',
        blank=True,
        default='',
        max_length=200
    )

    def __unicode__(self):
        return '%s,%s' % (self.refunded_name, self.refunded_address)

    class Meta:
        verbose_name = '邮寄信息'
        verbose_name_plural = verbose_name


class UserRefundedInfo(models.Model):
    order = models.OneToOneField(
        'main.Order',
        verbose_name='所属订单',
        related_name='user_refunded_info',
        null=True,
        blank=True
    )
    user_express_id = models.CharField(
        '快递单号',
        max_length=100,
    )
    user_express = models.CharField(
        '快递',
        max_length=100
    )
    remark = models.CharField(
        '备注',
        default='',
        max_length=100,
        blank=True
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )

    def __unicode__(self):
        return self.user_express_id

    class Meta:
        verbose_name = '用户退货信息'
        verbose_name_plural = verbose_name
