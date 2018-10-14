# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-14 20:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0068_roomstyles_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketOrderContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consignee_name', models.CharField(default='', max_length=50, verbose_name='\u6536\u8d27\u4eba\u59d3\u540d')),
                ('consignee_address', models.CharField(default='', max_length=200, verbose_name='\u6536\u8d27\u5730\u5740')),
                ('consignee_phone', models.CharField(default='', max_length=15, verbose_name='\u6536\u8d27\u4eba\u7535\u8bdd')),
                ('order', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Order')),
            ],
            options={
                'verbose_name': '\u5546\u573a\u8ba2\u5355\u6536\u8d27\u4eba',
                'verbose_name_plural': '\u5546\u573a\u8ba2\u5355\u6536\u8d27\u4eba',
            },
        ),
        migrations.RemoveField(
            model_name='marketorderdetail',
            name='consignee_address',
        ),
        migrations.RemoveField(
            model_name='marketorderdetail',
            name='consignee_name',
        ),
        migrations.RemoveField(
            model_name='marketorderdetail',
            name='consignee_phone',
        ),
        migrations.AlterField(
            model_name='marketorderdetail',
            name='market_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='market_order_detail', to='main.Order', verbose_name='\u5546\u573a\u8ba2\u5355'),
        ),
    ]