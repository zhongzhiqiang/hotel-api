# coding:utf-8
# Time    : 2018/10/20 下午5:52
# Author  : Zhongzq
# Site    : 
# File    : notice.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db import models


class Notice(models.Model):

    content = models.CharField(
        '提醒内容',
        max_length=100,
    )

    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )

    operator_name = models.ForeignKey(
        'main.StaffProfile',
        null=True,
        blank=True,
        verbose_name='创建人'
    )
    is_active = models.BooleanField(
        "是否有效",
        default=True,
        help_text='是否有效,默认为有效'
    )

    class Meta:
        verbose_name = '站内提醒'
        verbose_name_plural = verbose_name
