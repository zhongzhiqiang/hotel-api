# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-28 22:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0041_auto_20180927_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelorder',
            name='contact_name',
            field=models.CharField(default='', max_length=50, verbose_name='\u8054\u7cfb\u4eba'),
        ),
        migrations.AddField(
            model_name='hotelorder',
            name='contact_phone',
            field=models.CharField(default='', max_length=20, verbose_name='\u8054\u7cfb\u7535\u8bdd'),
        ),
    ]
