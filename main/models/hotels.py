# coding:utf-8
from __future__ import unicode_literals

from django.db import models


class Hotel(models.Model):
    name = models.CharField(
        '宾馆名称',
        max_length=100,
    )
    address = models.CharField(
        u'地址',
        max_length=100
    )
    longitude = models.CharField(
        '经度',
        max_length=100,
        blank=True,
        null=True
    )
    latitude = models.CharField(
        '纬度',
        max_length=100,
        blank=True,
        null=True

    )
    hotel_profile = models.TextField(
        '宾馆简介'
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '宾馆信息'
        verbose_name_plural = verbose_name
