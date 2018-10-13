# coding:utf-8
from __future__ import unicode_literals

from django.db import models


class IntegralSettings(models.Model):
    integral = models.PositiveIntegerField(
        '积分',
    )
    money = models.DecimalField(
        '钱',
        default=0,
        max_digits=10,
        decimal_places=2,
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
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return '%f' % self.ratio

    @property
    def ratio(self):

        return self.money / self.integral

    class Meta:
        verbose_name = '积分配置'
        verbose_name_plural = verbose_name


class GrowthValueSettings(models.Model):
    min_growth_value = models.PositiveIntegerField(
        '最小成长值',
        default=0,
    )
    max_growth_value = models.PositiveIntegerField(
        '最大成长值',
        default=2**31,
        help_text='2147483647'
    )

    level = models.CharField(
        '等级',
        max_length=10,
        help_text='成长值对应等级'
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
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.level

    class Meta:
        verbose_name = '成长值对应等级'
        verbose_name_plural = verbose_name


class IntegralInfo(models.Model):
    user = models.OneToOneField(
        'main.Consumer',
        verbose_name='用户',
        on_delete=models.CASCADE,
        related_name='integral_info'
    )
    integral = models.PositiveIntegerField(
        '总积分',
        default=0,
        help_text='积分可以用于兑换物品'
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True
    )
    growth_value = models.PositiveIntegerField(
        '成长值',
        default=0,
        help_text='成长值等于所有积分'
    )

    class Meta:
        verbose_name = '用户积分'
        verbose_name_plural = verbose_name


class IntegralDetail(models.Model):

    DetailType = (
        (10, '增加'),
        (20, '消费')
    )

    consumer = models.ForeignKey(
        'main.Consumer',
        verbose_name='用户',
        on_delete=models.CASCADE,
    )
    integral = models.IntegerField(
        '积分情况',
        default=0,
    )
    integral_type = models.IntegerField(
        '积分类型',
        choices=DetailType,
        default=10,
    )
    remark = models.CharField(
        '备注',
        max_length=100,
        help_text='本次积分来源',
        default='',
        blank=True
    )
    create_time = models.DateTimeField(
        '消费时间',
        auto_now_add=True,
        help_text='消费时间'
    )
    left_integral = models.IntegerField(
        '剩余积分',
        default=0
    )

    def __unicode__(self):
        return self.remark

    class Meta:
        verbose_name = '积分明细'
        verbose_name_plural = verbose_name
