# coding:utf-8
# Time    : 2018/10/17 下午8:05
# Author  : Zhongzq
# Site    : 
# File    : beat_tasks.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime

from django.db import transaction
from main.schedul.celery_app import app
from main.models import Order
from main.common.defines import OrderStatus, OrderType
from main.common.utils import increase_room_num


@transaction.atomic
def increase_num(order):
    increase_room_num(order)


@app.task(name='beat_cancel_task')
def beat_cancel_task():
    # 利用延时任务，来判断是否超过20分钟。如果超过20分就取消订单。
    #
    order_list = Order.objects.filter(order_status=OrderStatus.pre_pay)

    for order in order_list:
        minutes = datetime.datetime.now() - order.create_time
        # 这里如果是住宿订单，需要把房间数加上来
        if minutes > datetime.timedelta(minutes=20):
            order.order_status = OrderStatus.pasted
            if order.order_type == OrderType.hotel:
                increase_num(order)
            order.save()
