# coding:utf-8
# Time    : 2018/9/28 下午10:39
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals
import logging

from rest_framework import views
from django.db import transaction
from django.http import HttpResponse

from main.apps.wx_pay.utils import WxpayServerPub

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
