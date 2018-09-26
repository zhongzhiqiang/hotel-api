# coding:utf-8
# Time    : 2018/9/26 上午10:01
# Author  : Zhongzq
# Site    : 
# File    : vip_members.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db import models


class VipSettings(models.Model):
    # 这个对应部分会员商品类型。必须关联
    vip_name = models.CharField(
        '会员名称',
        max_length=10,
    )
    hotel_discount = models.DecimalField(
        '酒店折扣',
        max_digits=5,
        decimal_places=2,
        help_text='酒店住宿折扣'
    )

    class Meta:
        verbose_name = '会员折扣配置'
        verbose_name_plural = verbose_name


class VipMember(models.Model):
    vip_no = models.CharField(
        '会员卡号',
        max_length=20,
        blank=True,
        null=True
    )
    vip_level = models.CharField(
        '会员等级',
        max_length=20,
    )