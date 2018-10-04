# coding:utf-8
# Time    : 2018/10/4 下午6:17
# Author  : Zhongzq
# Site    : 
# File    : celery_app.py
# Software: PyCharm
from __future__ import unicode_literals
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
from main.sched import celery_config

from celery import (
    Celery,
    platforms,
)
app = Celery()
app.config_from_object(celery_config)
platforms.C_FORCE_ROOT = True
django.setup()


if __name__ == '__main__':
    app.start()
