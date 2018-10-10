# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-10 21:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_auto_20181010_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='VipMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_no', models.CharField(blank=True, max_length=20, null=True, verbose_name='\u4f1a\u5458\u5361\u53f7')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('consumer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Consumer', verbose_name='\u5bf9\u5e94\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u4f1a\u5458\u4e2d\u5fc3',
                'verbose_name_plural': '\u4f1a\u5458\u4e2d\u5fc3',
            },
        ),
        migrations.CreateModel(
            name='VipSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip_name', models.CharField(max_length=10, unique=True, verbose_name='\u4f1a\u5458\u540d\u79f0')),
                ('hotel_discount', models.DecimalField(decimal_places=2, help_text='\u9152\u5e97\u4f4f\u5bbf\u6298\u6263', max_digits=5, verbose_name='\u9152\u5e97\u6298\u6263')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u4f1a\u5458\u6298\u6263\u914d\u7f6e',
                'verbose_name_plural': '\u4f1a\u5458\u6298\u6263\u914d\u7f6e',
            },
        ),
        migrations.AddField(
            model_name='goods',
            name='is_special',
            field=models.BooleanField(default=False, help_text='\u662f\u5426\u4e3a\u4f1a\u5458, \u5f53\u6b64\u4e3aTrue\u65f6\uff0c\u9700\u8981\u4f20\u9012\u4f1a\u5458\u6743\u76ca', verbose_name='\u662f\u5426\u4e3a\u4f1a\u5458'),
        ),
        migrations.AddField(
            model_name='vipmember',
            name='vip_level',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.VipSettings'),
        ),
        migrations.AddField(
            model_name='goods',
            name='vip_info',
            field=models.OneToOneField(blank=True, help_text='\u4f1a\u5458\u6743\u76ca', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.VipSettings'),
        ),
    ]