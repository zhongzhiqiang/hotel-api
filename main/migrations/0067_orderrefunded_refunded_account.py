# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-13 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0066_auto_20181013_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderrefunded',
            name='refunded_account',
            field=models.DateTimeField(blank=True, null=True, verbose_name='\u9000\u6b3e\u5230\u8d26\u65f6\u95f4'),
        ),
    ]
