# coding:utf-8
# Time    : 2018/9/28 下午10:39
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals
import logging
from decimal import Decimal
import datetime

from rest_framework import views, viewsets
from django.db import transaction
from django.http import HttpResponse

from main.apps.wx_pay.utils import WxpayServerPub
from main.common.defines import WeiXinCode, MarketOrderStatus, HotelOrderStatus
from main.models import MarketOrder, HotelOrder

logger = logging.getLogger("__name__")


class ReceiveWXNotifyView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        logger.info('request data: {}'.format(request.body))

        wx_pay_server = WxpayServerPub()
        wx_pay_server.save_data(request.body)
        wx_return_data = wx_pay_server.getData()

        logger.info("paresing data:{}".format(wx_return_data))
        check_data = {
            'return_code': wx_return_data.get('return_code'),
            'appid': wx_return_data.get('appid'),
            'mch_id': wx_return_data.get('mch_id'),
            'nonce_str': wx_return_data.get('nonce_str'),
            'sign': wx_return_data.get('sign')
        }
        wx_pay_server.returnParameters = check_data

        return_param = check_data.copy()

        if not wx_pay_server.checkSign():
            logger.info('check sign fail')
            return_param.update({
                'return_code': 'FAiL',
                'sign': wx_pay_server.get_sign(return_param)
            })
            ret_xml = wx_pay_server.array_to_xml(return_param)
            return HttpResponse(ret_xml)

        order_id = wx_return_data['out_trade_no'].split('_')[0]
        pay_money = Decimal(wx_return_data['total_fee']) / 100
        time_end = wx_return_data['time_end']
        logger.info("split order_id:{}".format(order_id))

        if order_id.startswith('market'):
            return_code = self.handler_market(order_id, time_end, pay_money)

        else:
            return_code = self.handler_hotel(order_id, time_end, pay_money)

        return_param.update({
            "return_code": return_code,
            "sign": wx_pay_server.get_sign(return_param)
        })
        ret_xml = wx_pay_server.array_to_xml(return_param)
        logger.info("return wx xml:{}".format(ret_xml))
        return HttpResponse(ret_xml)

    @staticmethod
    def handler_market(order_id, time_end, pay_money):
        market_order = MarketOrder.objects.filter(
            order_id=order_id, pay_money=pay_money).first()
        if market_order and market_order.status == MarketOrderStatus.unpay:
            market_order.status = MarketOrderStatus.wait_deliver
            market_order.pay_time = datetime.datetime.strptime(
                time_end, '%Y%m%d%H%M%S')
            market_order.save()

            return_code = WeiXinCode.success
        else:
            return_code = WeiXinCode.fail
        return return_code

    @staticmethod
    def handler_hotel(order_id, time_end, pay_money):
        hotel_order = HotelOrder.objects.filter(
            order_id=order_id, sale_price=pay_money).first()
        if hotel_order and hotel_order.status == HotelOrderStatus.unpay:
            hotel_order.status = HotelOrderStatus.check_to_be
            hotel_order.pay_time = datetime.datetime.strptime(
                time_end, '%Y%m%d%H%M%S')
            hotel_order.save()

            return_code = WeiXinCode.success
        else:
            return_code = WeiXinCode.fail
        return return_code


class OrderStatusSearchView(viewsets.GenericViewSet):

    queryset = ''
    serializer_class = ''