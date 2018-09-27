# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-27 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0040_auto_20180927_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketorder',
            name='order_id',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='\u8ba2\u5355\u53f7'),
        ),
        migrations.AlterField(
            model_name='marketorder',
            name='order_status',
            field=models.IntegerField(blank=True, choices=[(10, '\u672a\u652f\u4ed8'), (20, '\u5f85\u53d1\u8d27'), (30, '\u5f85\u6536\u8d27'), (40, '\u5df2\u5b8c\u6210'), (50, '\u5df2\u53d6\u6d88'), (60, '\u7b49\u5f85\u8bc4\u4ef7'), (70, '\u8bc4\u4ef7\u5b8c\u6210')], default=10, verbose_name='\u8ba2\u5355\u72b6\u6001'),
        ),
    ]
