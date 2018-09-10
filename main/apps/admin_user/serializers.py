# coding:utf-8
# Time    : 2018/9/10 下午5:40
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import logging

from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.transaction import atomic

from main.models import StaffProfile, Hotel

logger = logging.getLogger(__name__)


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = (
            "__all__"
        )


class CreateStaffProfileSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    username = serializers.CharField(
        source='user.username'
    )
    belong_hotel = serializers.CharField(
        source='belong_hotel.name'
    )

    def validate_belong_hotel(self, value):
        hotel = Hotel.objects.filter(name=value).first()
        if not hotel:
            raise serializers.ValidationError("所属宾馆不存在")
        return hotel

    @atomic
    def create(self, validated_data):
        hotel = validated_data.pop('belong_hotel', {}).get('name')
        user = self.context['request'].user
        if user.is_superuser is False and user.staffprofile and user.staffprofile.belong_hotel != hotel:
            raise serializers.ValidationError({"belong_hotel": "选择宾馆错误,当前用户只能够创建所属宾馆"})
        username = validated_data.pop('user', {}).get("username")
        password = validated_data.pop('password')

        user = User.objects.filter(username=username).first()
        if user:
            remark = '已存在用户:{}'.format(username)
            raise serializers.ValidationError(remark)

        try:
            kwargs = {
                "username": username,
                "is_active": True
            }
            user = User(**kwargs)
            user.set_password(password)
            user.save()
        except Exception as e:
            logger.error("创建用户失败:{},{}".format(username, e))
            raise serializers.ValidationError("创建用户失败")
        validated_data.update({"user": user, "belong_hotel": hotel})
        instance = super(CreateStaffProfileSerializer, self).create(validated_data)
        return instance

    class Meta:
        model = StaffProfile
        fields = (
            'id',
            'username',
            'password',
            'user_name',
            'sex',
            'belong_hotel'
        )
