# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-21 17:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20181121_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerbalance',
            name='message',
            field=models.CharField(default=0, max_length=500, verbose_name='\u6d88\u8d39\u5907\u6ce8'),
        ),
    ]
