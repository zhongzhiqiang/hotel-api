# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-12 23:11
from __future__ import unicode_literals

from django.db import migrations, models
import main.modelfields.JsonFields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0061_remove_consumer_is_vip'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staffprofile',
            options={'permissions': [('banner', '\u6a2a\u5e45\u9875'), ('hotel', '\u5bbe\u9986\u4e2d\u5fc3'), ('consumer', '\u5ba2\u6237\u4e2d\u5fc3'), ('role', '\u6743\u9650\u4e2d\u5fc3'), ('distribution', '\u5206\u9500\u4e2d\u5fc3'), ('integral', '\u79ef\u5206\u4e2d\u5fc3'), ('market', '\u5546\u57ce\u4e2d\u5fc3'), ('market_order', '\u5546\u57ce\u8ba2\u5355\u4e2d\u5fc3'), ('tags', '\u6807\u7b7e\u4e2d\u5fc3'), ('staff', '\u804c\u5458\u4e2d\u5fc3'), ('hotel_order', '\u4f4f\u5bbf\u8ba2\u5355'), ('vip_info', '\u4f1a\u5458\u4e2d\u5fc3')], 'verbose_name': '\u804c\u5458\u4fe1\u606f', 'verbose_name_plural': '\u804c\u5458\u4fe1\u606f'},
        ),
        migrations.AddField(
            model_name='goods',
            name='cover_image',
            field=models.CharField(default='', max_length=100, verbose_name='\u5c01\u9762\u56fe'),
        ),
        migrations.AddField(
            model_name='goods',
            name='images',
            field=main.modelfields.JsonFields.JSONField(blank=True, default=[], null=True, verbose_name='\u6240\u6709\u56fe\u7247'),
        ),
    ]