# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-05 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20180905_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='distributionbonusdetail',
            old_name='bonus_detail',
            new_name='use_bonus',
        ),
        migrations.AddField(
            model_name='distributionbonuspick',
            name='pick_order',
            field=models.CharField(blank=True, db_index=True, error_messages={'unique': '\u8ba2\u5355\u53f7\u9519\u8bef'}, max_length=20, null=True, unique=True, verbose_name='\u63d0\u53d6\u8ba2\u5355\u53f7'),
        ),
    ]