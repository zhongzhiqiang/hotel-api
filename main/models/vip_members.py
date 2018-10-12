# coding:utf-8
# Time    : 2018/9/26 上午10:01
# Author  : Zhongzq
# Site    : 
# File    : vip_members.py
# Software: PyCharm
from __future__ import unicode_literals

from datetime import datetime
import uuid

from django.db import models


class VipSettings(models.Model):
    # 这个对应部分会员商品类型。必须关联
    vip_name = models.CharField(
        '会员名称',
        max_length=10,
        unique=True
    )

    hotel_discount = models.DecimalField(
        '酒店折扣',
        max_digits=5,
        decimal_places=2,
        help_text='酒店住宿折扣'
    )

    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True
    )

    def __unicode__(self):
        return self.vip_name

    class Meta:
        verbose_name = '会员折扣配置'
        verbose_name_plural = verbose_name


class VipMember(models.Model):
    vip_no = models.CharField(
        '会员卡号',
        max_length=32,
        unique=True
    )
    consumer = models.OneToOneField(
        'main.Consumer',
        verbose_name='对应用户'
    )
    # 会员权益
    vip_level = models.OneToOneField(
        'main.VipSettings',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    update_time = models.DateTimeField(
        '更新时间',
        auto_now=True
    )

    @classmethod
    def make_vip_no(cls):
        order_time = datetime.now().strftime("%Y%m%d")
        return_order_id = uuid.uuid1().get_hex().upper()[:24]
        return order_time + return_order_id

    @property
    def discount(self):
        return self.vip_level.hotel_discount

    def __unicode__(self):
        return self.vip_no

    class Meta:
        verbose_name = '会员中心'
        verbose_name_plural = verbose_name
