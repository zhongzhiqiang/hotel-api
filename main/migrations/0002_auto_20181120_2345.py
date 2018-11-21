# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-20 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomstyles',
            name='style_name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='\u623f\u95f4\u7c7b\u578b'),
        ),
        migrations.AlterUniqueTogether(
            name='roomstyles',
            unique_together=set([('belong_hotel', 'style_name')]),
        ),
    ]