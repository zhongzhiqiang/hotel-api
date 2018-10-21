# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-21 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0083_auto_20181020_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staffprofile',
            options={'permissions': [('banner', '\u6a2a\u5e45\u9875'), ('hotel', '\u5bbe\u9986\u4e2d\u5fc3'), ('consumer', '\u5ba2\u6237\u4e2d\u5fc3'), ('role', '\u6743\u9650\u4e2d\u5fc3'), ('distribution', '\u5206\u9500\u4e2d\u5fc3'), ('integral', '\u79ef\u5206\u4e2d\u5fc3'), ('market', '\u5546\u57ce\u4e2d\u5fc3'), ('market_order', '\u5546\u57ce\u8ba2\u5355\u4e2d\u5fc3'), ('tags', '\u6807\u7b7e\u4e2d\u5fc3'), ('staff', '\u804c\u5458\u4e2d\u5fc3'), ('hotel_order', '\u4f4f\u5bbf\u8ba2\u5355'), ('vip_info', '\u4f1a\u5458\u4e2d\u5fc3'), ('refunded', '\u9000\u6b3e\u4e2d\u5fc3'), ('comment_reply', '\u8bc4\u8bba\u56de\u590d\u4e2d\u5fc3')], 'verbose_name': '\u804c\u5458\u4fe1\u606f', 'verbose_name_plural': '\u804c\u5458\u4fe1\u606f'},
        ),
        migrations.AlterField(
            model_name='orderrefunded',
            name='refunded_message',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='\u9000\u6b3e\u63cf\u8ff0'),
        ),
    ]
