# coding:utf-8
# Time    : 2018/9/6 上午9:51
# Author  : Zhongzq
# Site    : 
# File    : views.py
# Software: PyCharm
from __future__ import unicode_literals
import logging

from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from main.apps.wx_auth import serializers
from main.models import Consumer, ConsumerBalance, VipMember

APP_ID = 'wx310b2c1f223f61c8'
APP_SECRET = 'af6d4f4c7c5fb0489deed97610e3064c'
PASSWORD = '123456789'
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
logger = logging.getLogger(__name__)


class WeiXinAuth(mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    """
    create:
        创建用户。返回登录token。利用wx.login返回的code换取token
    decrypt:
        解密用户数据。
    """
    queryset = Consumer.objects.all()
    serializer_class = serializers.ConsumerSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.WeiXinCreateTokenSerializer
        elif self.action == 'decrypt':
            return serializers.WeiXinDataDecrypt
        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wx_api = WXAPPAPI(appid=APP_ID, app_secret=APP_SECRET)
        data = serializer.data
        try:
            session_info = wx_api.exchange_code_for_session_key(data['code'])
        except Exception as e:
            logger.warning("exchange code error:{}".format(e))
            return Response(data={"code": ["登录失败"]}, status=status.HTTP_400_BAD_REQUEST)
        if session_info:
            openid = session_info['openid']
            user, _ = User.objects.get_or_create(
                defaults={"password": make_password(PASSWORD)}, username=openid)
            user_profile, _ = Consumer.objects.update_or_create(
                user=user, defaults={'openid': openid,
                                     'session_key': session_info['session_key'],
                                     'user_name': data['user_name'],
                                     "sex": data['sex'],
                                     "avatar_url": data['avatar_url']
                                     })
            if data.get("recommend_id") and not user_profile.sell_user:
                sell_user = Consumer.objects.get(id=data.get("recommend_id"))
                user_profile.sell_user = sell_user
                user_profile.save()
            serializer = JSONWebTokenSerializer(data={
                "username": openid, "password": PASSWORD
            })
            serializer.is_valid(raise_exception=True)
            user = serializer.object.get("user") or request.user
            token = serializer.object.get("token")
            response_data = jwt_response_payload_handler(token, user, request)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(data={"code": ['认证异常']}, status=status.HTTP_400_BAD_REQUEST)


class UserCenterView(mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    list:
        返回当前用户登录信息
    update_info:
        更新用户部分信息.
        ```
        SEX_STATUS = (
        (10, '未知'),
        (20, '男'),
        (30, '女')
        ) 传递字母
        ```
    update:
        这个接口不使用
    partial_update:
        这个接口不使用
    decrypt:
        解密用户用户，传递解密数据以及向量
    balance_info:
        返回用户的消费记录以及充值记录
    vip_info:
        返回当前用户的会员信息
    """
    queryset = Consumer.objects.all()
    serializer_class = serializers.ConsumerSerializer

    def get_serializer_class(self):
        if self.action == 'balance_info':
            return serializers.ConsumerBalanceSerializer
        elif self.action == 'vip_info':
            return serializers.VipMemberSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super(UserCenterView, self).get_queryset()
        if self.action == 'list':
            queryset = queryset.filter(user=self.request.user).prefetch_related('integral_info').first()
        elif self.action == 'balance_info':
            queryset = ConsumerBalance.objects.filter(consumer=self.request.user.consumer)
        elif self.action == 'vip_info':
            queryset = VipMember.objects.filter(consumer=self.request.user.consumer).first()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @list_route(methods=['POST'])
    def update_info(self, request, *args, **kwargs):
        self.kwargs['pk'] = self.request.user.consumer.id
        return self.partial_update(request, *args, **kwargs)

    @list_route(methods=['POST'])
    def decrypt(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wx_api = WXBizDataCrypt(appid=APP_ID, session_key=self.request.user.consumer.session_key)
        data = serializer.data
        try:
            result = wx_api.decrypt(data['encrypt_data'], data['iv'])
        except Exception as e:
            logger.exception("decrypt encrypt data error:{}".format(e))
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"encrypt_data": ['解密失败']})
        return Response(data=result, status=status.HTTP_200_OK)

    @list_route(methods=['GET'])
    def balance_info(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route(methods=['GET'])
    def vip_info(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
