# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ImagesModels(models.Model):

    image = models.ImageField(
        '图片'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(
        'content_type',
        'order_id',
    )

    def __unicode__(self):
        return '' % self.id

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name