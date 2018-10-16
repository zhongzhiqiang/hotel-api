# coding:utf-8
from __future__ import unicode_literals

from django.db import models

from main.modelfields.CompressionImageField import CompressionImageField


class Images(models.Model):
    image = CompressionImageField(
        '图片'
    )
    create_time = models.DateTimeField(
        '创建时间',
        auto_now_add=True
    )
    operator_name = models.ForeignKey(
        'main.StaffProfile',
        verbose_name='创建人员',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.image.url

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name
