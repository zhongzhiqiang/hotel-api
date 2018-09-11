# coding:utf-8
# Time    : 2018/8/28 下午3:32
# Author  : Zhongzq
# Site    : 
# File    : banners.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db import models


class Banners(models.Model):
    banner_title = models.CharField(
        '标题',
        max_length=100,
    )
    banner_images = models.CharField(
        '横幅图片',
        max_length=300,
        help_text='存储绝对路径'
    )
    jump_url = models.CharField(
        '跳转连接',
        max_length=300,
        blank=True,
        null=True,
        help_text='存储绝对路径'
    )
    is_show = models.BooleanField(
        '是否展示',
        default=False,
        help_text='是否可用在前端展示'
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
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.banner_title

    class Meta:
        verbose_name = 'banner'
        verbose_name_plural = verbose_name
