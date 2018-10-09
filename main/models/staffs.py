# coding:utf-8
# Time    : 2018/9/9 下午7:04
# Author  : Zhongzq
# Site    : 
# File    : staffs.py
# Software: PyCharm
from __future__ import unicode_literals

from django.db import models

from main.common.perms import ALL_PERMS


class StaffProfile(models.Model):
    SEX_CHOICE = (
        (10, '未知'),
        (20, '男'),
        (30, '女')
    )
    user = models.OneToOneField(
        'auth.User',
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='关联用户'
    )
    user_name = models.CharField(
        '用户信息',
        max_length=20
    )

    sex = models.IntegerField(
        '性别',
        choices=SEX_CHOICE,
        default=10,
    )
    belong_hotel = models.ForeignKey(
        'main.Hotel',
        null=True,
        blank=True,
        verbose_name='所属宾馆',
        on_delete=models.SET_NULL,
    )

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name = '职员信息'
        verbose_name_plural = verbose_name
        permissions = ALL_PERMS
