# coding:utf-8
# Time    : 2018/10/4 下午6:20
# Author  : Zhongzq
# Site    : 
# File    : pro.py
# Software: PyCharm
from __future__ import unicode_literals
REDIS_HOST = 'redis'
REDIS_PORT = '6379'
REDIS_PASSWORD = ''  # TODO
ALLOWED_HOSTS = ['*']
REDIS_HOST_PORT = '%s:%s' % (REDIS_HOST, REDIS_PORT)