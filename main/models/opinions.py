# coding:utf-8
# Time    : 2018/11/14 下午10:06
# Author  : Zhongzq
# Site    : 
# File    : opinions.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db import models


class Opinions(models.Model):
    consumer = models.ForeignKey(
        'main.Consumer',
        null=True,
        blank=True
    )
    content = models.CharField(
        '意见内容',
        max_length=200,
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )

    class Meta:
        verbose_name = '意见'
        verbose_name_plural = verbose_name
