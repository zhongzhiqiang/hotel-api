# coding:utf-8
from __future__ import unicode_literals

from django.db import models


class Consumer(models.Model):
    # 消费者的username为用户昵称或者账号。

    SEX_STATUS = (
        (10, '为止'),
        (20, '男'),
        (30, '女')
    )

    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    phone = models.CharField(
        '联系电话',
        max_length=15,
        blank='',
        default='',
    )
    user_name = models.CharField(
        '用户姓名',
        max_length=30,
    )

    sex = models.IntegerField(
        '性别',
        choices=SEX_STATUS,
        default=10,
    )

    contact_addr = models.CharField(
        '联系地址',
        max_length=100,
        blank='',
        default=''
    )

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = '消费者信息'
        verbose_name_plural = verbose_name
