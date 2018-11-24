# coding:utf-8
# Time    : 2018/10/15 下午9:24
# Author  : Zhongzq
# Site    : 
# File    : beat_task.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime
import logging

from main.schedul.celery_app import app
from main.models import Order
from main.apps.admin_integral.utils import make_integral, get_integral
from main.common.defines import OrderStatus, OrderType
from main.schedul.beat_tasks import increase_room_num
from main.common.utils import make_market_bonus
logger = logging.getLogger('celery')


@app.task(name='cancel_task')
def cancel_task(order_id):
    # 利用延时任务，来判断是否超过20分钟。如果超过20分就取消订单。
    #
    logger.info("start cancel task:{}".format(order_id))
    order = Order.objects.filter(order_id=order_id, order_status=OrderStatus.pre_pay).first()
    if not order:
        return ''

    minutes = datetime.datetime.now() - order.create_time
    if minutes > datetime.timedelta(minutes=20):
        logger.warning("cancel task:{} success".format(order_id))
        order.order_status = OrderStatus.pasted
        order.save()
        if order.order_type == OrderType.hotel:
            increase_room_num(order)

    logger.info("end cancel task:{} finish".format(order_id))


@app.task(name='make_integral_task')
def make_integral_task(order_id):
    # 3天后生成积分.
    order = Order.objects.get(order_id=order_id)
    # 生成积分.
    if order.order_status in (OrderStatus.success, OrderStatus.finish):
        # 生成积分。
        integral = get_integral(order.order_amount)
        remark = "购买商品:{},".format(integral)
        make_integral(order.consumer, integral, remark)
        if order.consumer.sell_user:
            make_market_bonus(order.consumer, order.consumer.sell_user, order)
            logger.info("deal order_id:{}, bonus".format(order_id))
        order.is_make = True
        logger.info("deal order_id:{}".format(order_id))
        order.save()
    else:
        return ''
