# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-06 21:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0097_auto_20181103_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributionapply',
            name='operator_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='\u64cd\u4f5c\u65f6\u95f4'),
        ),
    ]
