# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-02 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0094_auto_20181101_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminrefundedinfo',
            name='refunded_address',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='\u9000\u6b3e\u6536\u8d27\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='adminrefundedinfo',
            name='refunded_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='\u9000\u6b3e\u6536\u8d27\u4eba'),
        ),
        migrations.AlterField(
            model_name='adminrefundedinfo',
            name='refunded_phone',
            field=models.CharField(blank=True, default='', max_length=30, verbose_name='\u9000\u6b3e\u8054\u7cfb\u7535\u8bdd'),
        ),
    ]