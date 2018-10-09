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

from rest_framework import views
from rest_framework import response, status
from django.db import transaction
from django.http import HttpResponse

from main.apps.wx_pay.utils import WxpayServerPub
from main.common.defines import WeiXinCode, MarketOrderStatus, HotelOrderStatus
from main.models import MarketOrder, HotelOrder, ConsumerBalance, RechargeInfo
from main.apps.hotel_orders.serializers import HotelOrderSerializer
from main.apps.market_order.serializers import MarketOrderSerializer

logger = logging.getLogger("django")


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
        try:
            if order_id.startswith('market'):
                return_code = self.handler_market(order_id, time_end, pay_money)
            elif order_id.startswith('recharge'):
                return_code = self.handler_recharge(order_id, time_end, pay_money)
            else:
                return_code = self.handler_hotel(order_id, time_end, pay_money)
        except Exception:
            return_code = WeiXinCode.fail

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
        if market_order and market_order.order_status == MarketOrderStatus.unpay:
            market_order.order_status = MarketOrderStatus.wait_deliver
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
        if hotel_order and hotel_order.order_status == HotelOrderStatus.unpay:
            hotel_order.order_status = HotelOrderStatus.check_to_be

            hotel_order.pay_time = datetime.datetime.strptime(
                time_end, '%Y%m%d%H%M%S')
            hotel_order.save()

            params = {
                "consumer": hotel_order.consumer,
                "balance_type": 20,
                "message": "微信消费,预定房间:{},数量:{}".format(
                    hotel_order.hotelorderdetail.room_style.style_name, hotel_order.room_nums),
                "cost_price": -hotel_order.sale_price,
                "left_balance": hotel_order.consumer.balance,
            }
            ConsumerBalance(**params).save()
            return_code = WeiXinCode.success
        else:
            return_code = WeiXinCode.fail
        return return_code

    @staticmethod
    def handler_recharge(order_id, time_end, pay_money):
        recharge = RechargeInfo.objects.filter(
            order_id=order_id, recharge_money=pay_money
        ).prefetch_related('consumer').first()
        if recharge and recharge.recharge_status == 30:
            recharge.recharge_status = 10
            recharge.pay_time = datetime.datetime.strptime(time_end, '%Y%m%d%H%M%S')
            recharge.save()

            recharge.consumer.balance = recharge.consumer.balance + recharge.recharge_money
            recharge.consumer.free_balance = recharge.consumer.free_balance + recharge.free_money
            recharge.save()

            params = {
                "consumer": recharge.consumer,
                "balance_type": 10,
                "message": "微信消费,充值余额:{}, 赠送余额".format(recharge.recharge_money, recharge.free_money),
                "cost_price": recharge.recharge_money,
                "left_balance": recharge.consumer.balance,
            }
            ConsumerBalance(**params).save()
            return_code = WeiXinCode.success
        else:
            return_code = WeiXinCode.fail

        return return_code


class OrderStatusSearchView(views.APIView):

    SEARCH_TYPE = {
        "market": MarketOrder,
        "hotel": HotelOrder
    }
    serializer_map = {
        'market': MarketOrderSerializer,
        "hotel": HotelOrderSerializer
    }

    def get(self, request, *args, **kwargs):
        """
        传递数据 {
        order_id,
        search_type. 传递值:{market, hotel}
        }
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        order_id = self.request.query_params.get("order_id")
        search_type = self.request.query_params.get("search_type")

        if not order_id:
            return response.Response(data={"non_field_errors": ['请传递order_id']},
                                     status=status.HTTP_400_BAD_REQUEST)

        if not search_type or search_type not in self.SEARCH_TYPE.keys():
            return response.Response(data={"non_field_errors": ['请传递正确查询类型']},
                                     status=status.HTTP_400_BAD_REQUEST)

        model = self.SEARCH_TYPE[search_type]

        order_id = model.objects.filter(order_id=order_id).first()
        if not order_id:
            return response.Response(data={"non_field_errors": ['当前订单号不存在']},
                                     status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_map[search_type]
        serializer = serializer(instance=order_id)
        return response.Response(serializer.data)
