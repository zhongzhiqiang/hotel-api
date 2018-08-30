# coding:utf-8
from __future__ import unicode_literals

from django.db import models


class Images(models.Model):
    image = models.ImageField(
        '图片'
    )

    def __unicode__(self):
        return self.image.url

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name
