# coding:utf-8
from __future__ import unicode_literals

from django.db import models


class Tags(models.Model):
    name = models.CharField(
        '标签名称',
        unique=True,
        max_length=20,
        help_text='标签名称'
    )
    operator_name = models.ForeignKey(
        'main.Consumer',
        verbose_name='操作人',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
