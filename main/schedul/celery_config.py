# coding:utf-8
# Time    : 2018/10/4 下午6:18
# Author  : Zhongzq
# Site    : 
# File    : celery_config.py
# Software: PyCharm
from __future__ import unicode_literals

from celery.schedules import crontab
from main.config import config_module

host = config_module.REDIS_HOST
port = config_module.REDIS_PORT
password = config_module.REDIS_PASSWORD

CELERY_RESULT_BACKEND = 'redis://:%s@%s:%s/0' % (password, host, port)
BROKER_URL = 'redis://:%s@%s:%s/0' % (password, host, port)
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_TASK_RESULT_EXPIRES = 60 * 60

CELERY_IMPORTS = (
    'main.schedul.tasks',
    'main.schedul.beat_tasks'
)

CELERYBEAT_SCHEDULE = {
    "beat_cancel_task": {
        "task": "beat_cancel_task",
        "schedule": crontab(minute='*/20'),    # 每个小时0分执行一次任务
    },
    "auto_success": {
        "task": "auto_success",
        "schedule": crontab(hour=8, minute=0)
    },
    "auto_integral": {
        "task": "auto_integral",
        "schedule": crontab(hour='*/1', minute=0)
    }
}
