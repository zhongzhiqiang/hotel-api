# coding:utf-8
# Time    : 2018/10/4 下午6:19
# Author  : Zhongzq
# Site    : 
# File    : local.py
# Software: PyCharm
from __future__ import unicode_literals

CANCEL_TIME = 20 * 60

# redis config
REDIS_HOST = 'redis'
REDIS_PORT = '6379'
REDIS_PASSWORD = ''  # TODO
ALLOWED_HOSTS = ['*']
REDIS_HOST_PORT = '%s:%s' % (REDIS_HOST, REDIS_PORT)

MYSQL_DB = 'hotel'
MYSQL_HOST = 'mysql'
MYSQL_USER = 'root'
MYSQL_PORT = 3306
MYSQL_PWD = 'root'
