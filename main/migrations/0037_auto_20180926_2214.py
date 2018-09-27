# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-26 22:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_auto_20180926_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelorder',
            name='pay_type',
            field=models.IntegerField(choices=[(20, '\u4f59\u989d'), (30, '\u5fae\u4fe1\u652f\u4ed8')], default=30, help_text='\u9ed8\u8ba4\u5fae\u4fe1\u652f\u4ed8', verbose_name='\u652f\u4ed8\u7c7b\u578b'),
        ),
        migrations.AddField(
            model_name='hotelorder',
            name='refund_reason',
            field=models.CharField(blank=True, default='', help_text='\u9000\u6b3e\u65f6,\u5fc5\u987b\u586b\u5199', max_length=200, verbose_name='\u9000\u6b3e\u539f\u56e0'),
        ),
        migrations.AlterField(
            model_name='hotelorderdetail',
            name='belong_order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.HotelOrder', verbose_name='\u6240\u5c5e\u8ba2\u5355'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(help_text='\u6807\u7b7e\u540d\u79f0', max_length=20, unique=True, verbose_name='\u6807\u7b7e\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Consumer', verbose_name='\u64cd\u4f5c\u4eba'),
        ),
    ]