# coding:utf-8
# Time    : 2018/10/23 下午2:03
# Author  : Zhongzq
# Site    : 
# File    : logger_resp_ret.py
# Software: PyCharm

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

import logging

logger = logging.getLogger('django')


class LoggerMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        """
        Disconnects the signal receiver to prevent it from staying active.
        """
        logger.info("request return:{}".format(response))
        return response

    def process_request(self, request):
        if 'image' not in request.get_full_path():
            logger.info("request info body:{}, query:{},META:{}".format(request.body, request.GET, request.META))
        return None