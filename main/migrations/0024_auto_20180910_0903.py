# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-10 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_auto_20180909_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelorder',
            name='room_style_num',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='\u7528\u4e8e\u7edf\u8ba1\u8ba2\u5355\u6709\u591a\u5c11\u623f\u95f4', verbose_name='\u623f\u95f4\u7c7b\u578b\u6570\u91cf'),
        ),
    ]
