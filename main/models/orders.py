# coding:utf-8
from __future__ import unicode_literals

import datetime

from django.db import models


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
