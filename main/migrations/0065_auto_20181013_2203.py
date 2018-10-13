# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-13 22:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0064_auto_20181013_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegralInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('integral', models.PositiveIntegerField(default=0, help_text='\u79ef\u5206\u53ef\u4ee5\u7528\u4e8e\u5151\u6362\u7269\u54c1', verbose_name='\u603b\u79ef\u5206')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('growth_value', models.PositiveIntegerField(default=0, help_text='\u6210\u957f\u503c\u7b49\u4e8e\u6240\u6709\u79ef\u5206', verbose_name='\u6210\u957f\u503c')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='integral_info', to='main.Consumer', verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u79ef\u5206',
                'verbose_name_plural': '\u7528\u6237\u79ef\u5206',
            },
        ),
        migrations.RemoveField(
            model_name='integral',
            name='user',
        ),
        migrations.DeleteModel(
            name='Integral',
        ),
    ]
