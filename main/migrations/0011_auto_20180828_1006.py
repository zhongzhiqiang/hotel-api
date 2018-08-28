# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-28 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20180823_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='goods_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5546\u54c1\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='hotelorder',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u8ba2\u5355\u91d1\u989d'),
        ),
        migrations.AlterField(
            model_name='hotelorderdetail',
            name='room_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5165\u4f4f\u65f6\u623f\u95f4\u5355\u4ef7'),
        ),
        migrations.AlterField(
            model_name='roomstyles',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='\u5355\u4ef7'),
        ),
    ]
