# coding:utf-8
# Time    : 2018/9/6 上午9:52
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals

import uuid
import requests
from rest_framework import serializers
from django.core.files.base import ContentFile

from main.models import Consumer, ConsumerBalance, RechargeInfo, RechargeSettings, IntegralInfo, VipMember, Images
from main.apps.admin_images.serializers import CreateImageSerializer


class WeiXinCreateTokenSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=100, help_text='微信登录获取code')
    user_name = serializers.CharField(allow_blank=True, help_text='用户昵称')
    sex = serializers.CharField(allow_blank=True, help_text='性别')
    avatar_url = serializers.CharField(help_text='头像链接')

    def validate_user_name(self, attrs):
        if not attrs:
            attrs = uuid.uuid1()
        return attrs

    def validate_avatar_url(self, attrs):
        request = self.context['request']
        try:
            resp = requests.get(attrs)
            image = resp.content
            image = ContentFile(content=image, name='avatar_url')
            image_serializer = CreateImageSerializer(data={"image": image})
            image_serializer.is_valid(raise_exception=True)
            instance = image_serializer.save()

            attrs = request.build_absolute_uri(instance.image.url)
        except Exception:
            attrs = ""
        return attrs

    def validate_sex(self, attr):
        try:
            attr = int(attr)
        except:
            attr = 0
        if attr == 0:
            attr = 10
        elif attr == 1:
            attr = 20
        else:
            attr = 30
        return attr


class WeiXinDataDecrypt(serializers.Serializer):
    encrypt_data = serializers.CharField(help_text='微信加密数据')
    iv = serializers.CharField(help_text='向量')


class IntegralSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegralInfo
        fields = "__all__"


class ConsumerSerializer(serializers.ModelSerializer):
    sex_display = serializers.CharField(
        source='get_sex_display',
        read_only=True
    )
    sell_user_name = serializers.CharField(
        source='sell_user.user_name',
        read_only=True
    )
    integral_info = IntegralSerializer(read_only=True)

    class Meta:
        model = Consumer
        fields = (
            'id',
            'phone',
            'user_name',
            'sex',
            'contact_addr',
            'is_distribution',
            'sell_user',
            'sex_display',
            'bonus',
            'sell_user',
            'sell_user_name',
            'balance',
            'recharge_balance',
            'free_balance',
            'integral',
            'integral_info'
        )
        read_only_fields = ('is_distribution', 'sell_user', 'bonus', 'free_balance', 'recharge_balance')


class ConsumerBalanceSerializer(serializers.ModelSerializer):
    # 用户余额详情
    balance_type_display = serializers.CharField(
        source='get_balance_type_display',
        read_only=True
    )

    class Meta:
        model = ConsumerBalance
        fields = (
            'id',
            'balance_type',
            'balance_type_display',
            'message',
            'cost_price',
            'create_time',
            'left_balance'
        )


class CreateRechargeSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        recharge_money = validated_data["recharge_money"]
        discount = RechargeSettings.objects.filter(recharge_price=recharge_money).first()
        if not discount:
            raise serializers.ValidationError("充值金额错误")
        validated_data.update({"free_money": discount.free_balance})
        instance = super(CreateRechargeSerializer, self).create(validated_data)
        instance.order_id = instance.make_order()
        instance.save()
        return instance

    class Meta:
        model = RechargeInfo
        fields = (
            'id',
            'order_id',
            'recharge_money',
            'free_money'
        )
        read_only_fields = ("free_money", )


class RechargeInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RechargeInfo
        fields = "__all__"


class RechargeSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeSettings
        fields = "__all__"


class VipMemberSerializer(serializers.ModelSerializer):

    vip_name = serializers.CharField(
        source='vip_level.vip_name',
        read_only=True
    )

    class Meta:
        model = VipMember
        fields = (
            'id',
            'vip_no',
            'vip_level',
            'create_time',
            'discount',
            'vip_name'
        )
