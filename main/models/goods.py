# coding:utf-8
from __future__ import unicode_literals

from django.db import models

from main.modelfields.JsonFields import JSONField


class GoodsCategory(models.Model):

    category_name = models.CharField(
        '分类名称',
        max_length=10
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    is_active = models.BooleanField(
        '是否上架',
        default=False,
        help_text='默认不上架',
        blank=True
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True,
        blank=True,
        null=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.category_name

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name


class Goods(models.Model):
    METHOD = (
        ('no', '不参与'),
        ('fixed', '固定'),
        ('ratio', '比例')
    )

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
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    is_integral = models.BooleanField(
        '是否为积分兑换',
        default=False,
        blank=True
    )
    is_promotion = models.BooleanField(
        '是否促销',
        default=False,
        blank=True
    )
    is_special = models.BooleanField(
        '是否为会员',
        help_text='是否为会员, 当此为True时，需要传递会员权益',
        default=False
    )
    vip_info = models.OneToOneField(
        'main.VipSettings',
        null=True,
        blank=True,
        help_text='会员权益'
    )
    # 商品实际所付等于
    need_integral = models.PositiveIntegerField(
        '所需积分',
        default=0,
        blank=True
    )
    distribution_method = models.CharField(
        '分销方式',
        choices=METHOD,
        default='no',
        max_length=10
    )
    distribution_calc = models.DecimalField(
        '分销奖金',
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        help_text='分销金额计算，如果是固定是单件商品价格，如果是比例这是销售价格的比例'
    )

    is_active = models.BooleanField(
        '是否上架',
        default=False,
        blank=True
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True,
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True,
        blank=True
    )
    cover_image = models.CharField(
        '封面图',
        max_length=100,
        default=''
    )
    images = JSONField(
        '所有图片',
        default=[],
        blank=True,
        null=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.goods_name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = verbose_name
