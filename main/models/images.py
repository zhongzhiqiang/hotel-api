# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django_thumbs.db.models import ImageWithThumbsField


class Images(models.Model):
    image = ImageWithThumbsField(
        '图片',
        sizes=((125, 125), (200, 200))
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
