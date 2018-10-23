# coding:utf-8
# Time    : 2018/9/26 下午5:00
# Author  : Zhongzq
# Site    : 
# File    : utils.py
# Software: PyCharm
from __future__ import unicode_literals
from main.models import IntegralDetail, VipMember


def create_balance_info(user, integral, integral_type, remark):
    # 生成用户余额详情。
    params = {
        "consumer": user,
        "integral": integral,
        "integral_type": integral_type,
        "remark": remark,
    }


def create_integral_info(consumer, integral, integral_type, remark):
    params = {
        "consumer": consumer,
        "integral": integral,
        "remark": remark,
        "integral_type": integral_type,
        "left_integral": consumer.integral
    }
    IntegralDetail.objects.create(**params)


def get_goods_name_by_post(market_order_detail, goods_type):
    """
    通过商场的信息来获取
    :param market_order_detail: 
    :param goods_type: 
    :return: 
    """
    goods_name = u''
    num = 0
    if goods_type == 'integral':
        for market in market_order_detail:
            if market['goods'].is_integral:
                num += market['nums']
                if goods_name:
                    goods_name = goods_name + u',' + market['goods'].goods_name
                else:
                    goods_name = market['goods'].goods_name
    else:
        for market in market_order_detail:
            if not market['goods'].is_integral:
                num += market['nums']
                if goods_name:
                    goods_name = goods_name + u',' + market['goods'].goods_name
                else:
                    goods_name = market['goods'].goods_name

    return goods_name, num


def get_goods_name_by_instance(market_order_detail, goods_type):
    """
    重新支付时需要的生成商品名称
    :param market_order_detail: 
    :param goods_type: 
    :return: 
    """
    goods_name = u''
    num = 0
    if goods_type == 'integral':
        for market in market_order_detail:
            if market.goods.is_integral:
                num += market.nums
                if goods_name:
                    goods_name = goods_name + u',' + market.goods.goods_name
                else:
                    goods_name = market.goods.goods_name
    else:
        for market in market_order_detail:
            if not market.goods.is_integral:
                num += market.nums
                if goods_name:
                    goods_name = goods_name + u',' + market.goods.goods_name
                else:
                    goods_name = market.goods.goods_name

    return goods_name, num


def create_vip(consumer, vip_level):
    # 创建VIP信息
    params = {
        "consumer": consumer,
        "vip_level": vip_level,
        "vip_no": VipMember.make_vip_no()
    }
    vip_member = VipMember.objects.filter(consumer=consumer).first()
    if vip_member:
        vip_member.vip_level = vip_level
        vip_member.save()
    else:
        VipMember.objects.create(**params)


def increase_room_num(order):
    # 增加房间类型
    """
    :param order: 订单模型
    :return: 
    """
    room_style = order.hotel_order_detail.room_style
    room_style.room_count = room_style.room_count + order.hotel_order_detail.room_nums
    room_style.save()


def reduce_room_num(room_style, room_nums):
    """
    支付成功减去房间数
    :param room_style: 房间类型的
    :param room_nums: 订单房间数
    :return: 
    """
    # 下单支付成功扣除房间数
    room_style.room_count = room_style.room_count - room_nums
    room_style.save()
