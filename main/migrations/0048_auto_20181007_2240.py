# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-07 22:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20181007_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_time', models.DateTimeField(auto_now_add=True, verbose_name='\u56de\u590d\u65f6\u95f4')),
                ('reply_content', models.CharField(max_length=200, verbose_name='\u56de\u590d\u5185\u5bb9')),
            ],
            options={
                'verbose_name': '\u8bc4\u8bba\u56de\u590d',
                'verbose_name_plural': '\u8bc4\u8bba\u56de\u590d',
            },
        ),
        migrations.CreateModel(
            name='HotelOrderComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_show', models.IntegerField(choices=[(10, '\u8bc4\u8bba\u4eba\u53ef\u89c1'), (20, '\u6240\u6709\u4eba\u53ef\u89c1')], default=10, help_text='\u9ed8\u8ba4\u53ea\u80fd\u591f\u8bc4\u8bba\u4eba\u53ef\u89c1', verbose_name='\u8bc4\u8bba\u53ef\u89c1')),
                ('content', models.CharField(default='', max_length=200, verbose_name='\u8bc4\u8bba\u5185\u5bb9')),
                ('comment_level', models.IntegerField(choices=[(10, '\u4e00\u661f'), (20, '\u4e24\u661f'), (30, '\u4e09\u661f'), (40, '\u56db\u661f'), (50, '\u4e94\u661f')], default=50, verbose_name='\u8bc4\u8bba\u7b49\u7ea7')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4')),
                ('no_show_reason', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='\u4e0d\u663e\u793a\u539f\u56e0')),
                ('belong_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.HotelOrder', verbose_name='\u5173\u8054\u8ba2\u5355')),
                ('commenter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Consumer', verbose_name='\u8bc4\u8bba\u4eba')),
            ],
            options={
                'verbose_name': '\u8ba2\u5355\u8bc4\u8bba\u56de\u590d',
                'verbose_name_plural': '\u8ba2\u5355\u8bc4\u8bba\u56de\u590d',
            },
        ),
        migrations.AddField(
            model_name='commentreply',
            name='comment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.HotelOrderComment'),
        ),
        migrations.AddField(
            model_name='commentreply',
            name='reply_staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.StaffProfile', verbose_name='\u56de\u590d\u4eba'),
        ),
    ]