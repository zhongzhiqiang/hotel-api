# coding:utf-8
# Time    : 2018/10/17 下午8:05
# Author  : Zhongzq
# Site    : 
# File    : beat_tasks.py
# Software: PyCharm
from __future__ import unicode_literals
import datetime
import logging

from django.db import transaction
from main.schedul.celery_app import app
from main.models import Order
from main.common.defines import OrderStatus, OrderType
from main.common.utils import increase_room_num, get_goods_name_by_instance, make_market_bonus
from main.apps.admin_integral.utils import make_integral, get_integral


logger = logging.getLogger('celery')


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
            logger.info("cancel order_id:{}".format(order.order_id))
            if order.order_type == OrderType.hotel:
                increase_num(order)
            order.save()


@app.task(name='auto_success')
@transaction.atomic
def auto_success():
    # 查询所有的入住中的订单。判断退房时间，如果退房时间为当天。则将当前订单置为完成
    order_list = Order.objects.filter(order_status=OrderStatus.check_in, order_type=OrderType.hotel)
    now = datetime.datetime.now()
    for order in order_list:
        order_detail = order.hotel_order_detail
        checkout_time = order_detail.reserve_check_out_time

        if now.year == checkout_time.year and now.month == checkout_time.month and now.day == checkout_time.day:
            order.order_status = OrderStatus.success
            increase_room_num(order)
            # 生成积分
            integral = get_integral(order.order_amount)
            remark = "住宿:%s,积分:%s" % (order.hotel_order_detail.room_style.style_name, integral)
            make_integral(order.consumer, integral, remark)
            order.save()


@app.task(name='auto_delivery')
def auto_delivery():
    # 自动收货
    order_list = Order.objects.filter(order_status=OrderStatus.take_deliver, order_type=OrderType.market)

    now = datetime.datetime.now()
    for order in order_list:
        operator_time = order.operator_time
        deliver_day = operator_time + datetime.timedelta(days=7)

        if now.year == deliver_day.year and now.month == deliver_day.month and now.day == deliver_day.day:
            order.order_status = OrderStatus.success
            order.operator_time = datetime.datetime.now()
            order.save()


@app.task(name='auto_integral')
def auto_integral():
    status = [OrderStatus.success, OrderStatus.finish]
    order_list = Order.objects.filter(order_status__in=status, order_type=OrderType.market, is_make=False)
    now = datetime.datetime.now()

    for order in order_list:
        operator_time = order.operator_time
        # TODO 这里需要更改
        # integral_day = operator_time + datetime.timedelta(days=7)
        integral_day = operator_time + datetime.timedelta(minutes=1)
        if now.year == integral_day.year and now.month == integral_day.month and now.day == integral_day.day:
            integral = get_integral(order.order_amount)
            name = get_goods_name_by_instance(order.market_order_detail.all(), 'market')
            remark = "购买商品:{},积分:{}".format(name, integral)
            make_integral(order.consumer, integral, remark)
            logger.info("{}, make integral:{}".format(order.consumer, remark,))
            if order.consumer.sell_user:
                make_market_bonus(order.consumer, order.consumer.sell_user, order)
            order.is_make = True
            order.save()

if __name__ == '__main__':
    auto_success()
