# coding:utf-8
# Time    : 2018/10/4 下午6:19
# Author  : Zhongzq
# Site    : 
# File    : local.py
# Software: PyCharm
from __future__ import unicode_literals

CANCEL_TIME = 20 * 60

# redis config
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PASSWORD = ''  # TODO
ALLOWED_HOSTS = ['*']
REDIS_HOST_PORT = '%s:%s' % (REDIS_HOST, REDIS_PORT)
