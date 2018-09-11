# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-11 11:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_hotel_tel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumer',
            options={'verbose_name': '\u5ba2\u6237\u4fe1\u606f', 'verbose_name_plural': '\u5ba2\u6237\u4fe1\u606f'},
        ),
        migrations.AddField(
            model_name='banners',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='distributionapply',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='distributionbonusdetail',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='distributionbonuspick',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile', verbose_name='\u64cd\u4f5c\u4eba\u5458'),
        ),
        migrations.AddField(
            model_name='distributionbonuspick',
            name='operator_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u64cd\u4f5c\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='goods',
            name='create_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2018, 9, 11, 11, 30, 39, 440936), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goods',
            name='operator_time',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='goods',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='goodscategory',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='goodscategory',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='growthvaluesettings',
            name='create_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2018, 9, 11, 11, 30, 45, 603800), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='growthvaluesettings',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='growthvaluesettings',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='create_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2018, 9, 11, 11, 30, 48, 225441), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hotel',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u5bf9\u5916\u5f00\u653e'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile', verbose_name='\u64cd\u4f5c\u4eba\u5458'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='hotelorder',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='images',
            name='create_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2018, 9, 11, 11, 30, 49, 727787), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='images',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile', verbose_name='\u521b\u5efa\u4eba\u5458'),
        ),
        migrations.AddField(
            model_name='integralsettings',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='create_time',
            field=models.DateTimeField(auto_created=True, default=datetime.datetime(2018, 9, 11, 11, 30, 51, 641024), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rooms',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='update_time',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 9, 11, 11, 30, 54, 33237), verbose_name='\u66f4\u65b0\u65f6\u95f4'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roomstyles',
            name='operator_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.StaffProfile'),
        ),
        migrations.AddField(
            model_name='roomstyles',
            name='update_time',
            field=models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='rooms',
            name='room_status',
            field=models.IntegerField(choices=[(10, '\u672a\u5165\u4f4f'), (20, '\u5df2\u9884\u5b9a'), (30, '\u5165\u4f4f'), (40, '\u9000\u623f'), (50, '\u7ef4\u4fee')], default=10, verbose_name='\u623f\u95f4\u72b6\u6001'),
        ),
    ]
