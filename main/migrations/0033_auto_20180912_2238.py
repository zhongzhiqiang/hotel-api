# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-12 22:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_auto_20180912_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomstyles',
            name='style_name',
            field=models.CharField(db_index=True, max_length=100, unique=True, verbose_name='\u623f\u95f4\u7c7b\u578b'),
        ),
    ]