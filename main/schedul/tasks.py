# coding:utf-8
# Time    : 2018/10/15 下午9:24
# Author  : Zhongzq
# Site    : 
# File    : beat_task.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime

from main.schedul.celery_app import app
from main.models import Order, IntegralDetail
from main.apps.admin_integral.utils import make_integral, get_integral
from main.common.defines import OrderStatus


@app.task()
def cancel_task(order_id):
    # 利用延时任务，来判断是否超过20分钟。如果超过20分就取消订单。
    #
    order = Order.objects.filter(order_id=order_id, order_status=OrderStatus.pre_pay).first()
    if not order:
        return ''

    minutes = order.create_time - datetime.datetime.now()
    if minutes > datetime.timedelta(minutes=20):
        order.order_status = OrderStatus.pasted
        order.save()
    else:
        # 再继续延迟执行
        cancel_task.apply_async(args=(order_id, ), countdown=minutes.total_seconds())


@app.task()
def make_integral_task(order_id):
    # 3天后生成积分.
    order = Order.objects.get(order_id=order_id)
    # 生成积分.
    if order.order_status in (OrderStatus.success, OrderStatus.finish):
        # 生成积分。
        integral = get_integral(order.order_amount)
        remark = "购买商品:{},".format(integral)
        make_integral(order.consumer, integral, remark)
    else:
        return ''
