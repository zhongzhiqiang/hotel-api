# coding:utf-8
# Time    : 2018/10/3 下午3:47
# Author  : Zhongzq
# Site    : 
# File    : recharge.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db import models


class RechargeSettings(models.Model):

    free_balance = models.DecimalField(
        '赠送余额',
        max_digits=5,
        decimal_places=2,
    )
    recharge_price = models.DecimalField(
        '充值金额',
        max_digits=5,
        decimal_places=2,
    )

    operator_name = models.ForeignKey(
        'main.StaffProfile',
        verbose_name='操作人员',
        blank=True,
        null=True
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True
    )
    is_active = models.BooleanField(
        '是否启用',
        default=True,
    )

    class Meta:
        verbose_name = '充值配置'
        verbose_name_plural = verbose_name
