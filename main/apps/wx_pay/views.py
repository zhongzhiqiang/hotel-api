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
from main.common.defines import WeiXinCode, OrderStatus, OrderType, PayType, RefundedStatus
from main.models import Order, ConsumerBalance, RechargeInfo, OrderPay, IntegralDetail, WeiXinPayInfo, OrderRefunded
from main.apps.orders import serializers
from main.common import utils
from main.common.decrypt import ASECipher

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

        logger.info("wx_return_data:{}".format(wx_return_data))

        order_id = wx_return_data['out_trade_no'].split('_')[0]
        pay_money = Decimal(wx_return_data['total_fee']) / 100
        time_end = wx_return_data['time_end']
        logger.info("split order_id:{}".format(order_id))
        try:
            if order_id.startswith('recharge'):
                return_code = self.handler_recharge(order_id, time_end, pay_money)
            else:
                return_code = self.handler_order(order_id, time_end, pay_money, wx_return_data)
        except Exception as e:
            logger.error("error:{}".format(e), exc_info=True)
            return_code = WeiXinCode.fail

        return_param.update({
            "return_code": return_code,
            "sign": wx_pay_server.get_sign(return_param)
        })
        ret_xml = wx_pay_server.array_to_xml(return_param)

        logger.info("return wx xml:{}".format(ret_xml))
        return HttpResponse(ret_xml)

    @staticmethod
    def handler_order(order_id, time_end, pay_money, wx_return_data):
        logger.info("order_id:{}, wx_return_data:{}".format(order_id, wx_return_data))
        if order_id.startswith("wx"):
            wx_pay = WeiXinPayInfo.objects.filter(wx_order_id=order_id).first()
            hotel_order = wx_pay.order
            wx_pay.call_back_result = wx_return_data.get("return_code") or ''
            wx_pay.call_back_result_code = wx_return_data.get("result_code") or ''
            wx_pay.call_return_msg = wx_return_data.get("return_msg") or ''
            wx_pay.save()
        else:
            hotel_order = Order.objects.filter(
                order_id=order_id, order_amount=pay_money, pay_type=PayType.weixin).first()

        if hotel_order and hotel_order.order_status == OrderStatus.pre_pay and hotel_order.order_type == OrderType.hotel:
            hotel_order.order_status = OrderStatus.to_check_in

            hotel_order.pay_time = datetime.datetime.strptime(
                time_end, '%Y%m%d%H%M%S')
            hotel_order.save()

            params = {
                "consumer": hotel_order.consumer,
                "balance_type": 20,
                "message": "微信消费,预定房间:{},数量:{}".format(
                    hotel_order.hotel_order_detail.room_style.style_name, hotel_order.num),
                "cost_price": -hotel_order.order_amount,
                "left_balance": hotel_order.consumer.balance,
            }
            ConsumerBalance(**params).save()
            return_code = WeiXinCode.success
        elif hotel_order and hotel_order.order_status == OrderStatus.pre_pay and hotel_order.order_type == OrderType.market:

            # 这里判断商品里面是否有会员

            # 这里要处理积分判断兑换的问题。并生成积分的扣除
            goods_name = utils.get_goods_name_by_instance(hotel_order.market_order_detail.all(), 'market')
            for market in hotel_order.market_order_detail.all():
                if market.is_special:
                    utils.create_vip(hotel_order.consumer, market.vip_info)
            if hotel_order.integral:
                # 这里扣去积分
                hotel_order.consumer.integral_info.integral = hotel_order.consumer.integral - hotel_order.integral
                hotel_order.consumer.integral_info.save()
                integral = {
                    "consumer": hotel_order.consumer,
                    "integral": -hotel_order.integral,
                    "integral_type": 20,
                    "remark": "商品消费,购买商品:{}".format(hotel_order.integral),
                    "left_integral": hotel_order.consumer.integral,
                }
                IntegralDetail.objects.create(**integral)
            hotel_order.order_status = OrderStatus.deliver
            hotel_order.pay_time = datetime.datetime.strptime(
                time_end, '%Y%m%d%H%M%S')
            hotel_order.save()
            return_code = WeiXinCode.success
            params = {
                "consumer": hotel_order.consumer,
                "balance_type": 20,
                "message": "微信消费,购买商品:{},数量:{}".format(
                    goods_name, hotel_order.num),
                "cost_price": -hotel_order.order_amount,
                "left_balance": hotel_order.consumer.balance,
            }
            ConsumerBalance(**params).save()
        else:
            return_code = WeiXinCode.fail
            logger.warning("post error:{}".format(wx_return_data))
        # 支付成功时，创建支付信息.
        if return_code == WeiXinCode.success:
            pay_info = {
                "wx_order_id": wx_return_data.get('transaction_id') or '',
                "order": hotel_order,
                "money": pay_money,
                "integral": hotel_order.integral
            }
            OrderPay.objects.create(**pay_info)
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

        if not order_id:
            return response.Response(data={"non_field_errors": ['请传递order_id']},
                                     status=status.HTTP_400_BAD_REQUEST)

        order_id = Order.objects.filter(order_id=order_id).first()
        if not order_id:
            return response.Response(data={"non_field_errors": ['当前订单号不存在']},
                                     status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.OrderSerializer
        serializer = serializer(instance=order_id)
        return response.Response(serializer.data)


class RefundedNotifyView(views.APIView):
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        logger.info('request data: {}'.format(request.body))

        wx_pay_server = WxpayServerPub()
        wx_pay_server.save_data(request.body)
        wx_return_data = wx_pay_server.getData()

        logger.info("paresing data:{}".format(wx_return_data))
        aes_cipher = ASECipher('')
        return_param = {"return_code": WeiXinCode.fail}
        if wx_return_data == WeiXinCode.success:
            req_info = wx_return_data['req_info']
            ret = aes_cipher.decrypt(req_info)
            out_refund_no = ret['out_refund_no']
            success_time = ret['success_time']

            order_refunded = OrderRefunded.objects.get(refunded_order_id=out_refund_no)

            order_refunded.refunded_status = RefundedStatus.success
            order_refunded.refunded_account = datetime.datetime.strptime(success_time, '%Y-%m-%d %H:%M:%S')
            order_refunded.save()
            order_refunded.order.order_status = OrderStatus.refunded
            order_refunded.order.save()
            return_param.update({"return_code": WeiXinCode.success})
        ret_xml = wx_pay_server.array_to_xml(return_param)

        logger.info("return wx xml:{}".format(ret_xml))
        return HttpResponse(ret_xml)
