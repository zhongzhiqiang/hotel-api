# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-17 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0080_marketorderexpress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distributionapply',
            name='apply_status',
            field=models.IntegerField(choices=[(10, '\u63d0\u4ea4\u6210\u529f'), (20, '\u62d2\u7edd'), (30, '\u5b8c\u6210'), (40, '\u64a4\u56de\u7533\u8bf7')], default=10, verbose_name='\u7533\u8bf7\u72b6\u6001'),
        ),
    ]