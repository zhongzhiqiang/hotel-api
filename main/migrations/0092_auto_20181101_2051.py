# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-01 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0091_auto_20181101_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelordercomment',
            name='comment_level',
            field=models.IntegerField(choices=[(1, '\u4e00\u5206'), (2, '\u4e24\u5206'), (3, '\u4e09\u5206'), (4, '\u56db\u5206'), (5, '\u4e94\u5206')], default=5, verbose_name='\u8bc4\u8bba\u7b49\u7ea7'),
        ),
    ]
