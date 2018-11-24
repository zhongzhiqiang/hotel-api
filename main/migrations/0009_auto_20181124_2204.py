# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-24 22:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20181124_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelordercomment',
            name='goods',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Goods'),
        ),
        migrations.AlterField(
            model_name='hotelordercomment',
            name='belong_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Order', verbose_name='\u5173\u8054\u8ba2\u5355'),
        ),
    ]
