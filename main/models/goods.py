# coding:utf-8
from __future__ import unicode_literals

from django.db import models


class GoodsCategory(models.Model):

    category_name = models.CharField(
        '分类名称',
        max_length=10
    )
    create_time = models.DateTimeField(
        auto_now_add=True
    )
    is_active = models.BooleanField(
        '是否上架',
        default=False,
        help_text='默认不上架',
        blank=True
    )

    def __unicode__(self):
        return self.category_name

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


class Goods(models.Model):

    category = models.ForeignKey(
        'main.GoodsCategory',
        models.CASCADE,
        verbose_name='商品分类',
        related_name='goods'
    )
    goods_name = models.CharField(
        '商品名称',
        max_length=100,
    )
    goods_price = models.DecimalField(
        '商品价格',
        max_digits=5,
        decimal_places=2
    )
    is_integral = models.BooleanField(
        '是否可以积分兑换',
        default=False,
        blank=True
    )
    # 商品实际所付等于
    need_integral = models.PositiveIntegerField(
        '所需最大积分',
        default=0,
        blank=True
    )
    is_active = models.BooleanField(
        '是否上架',
        default=False,
        blank=True
    )

    def __unicode__(self):
        return self.goods_name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
