# coding:utf-8
# Time    : 2018/9/10 下午5:40
# Author  : Zhongzq
# Site    : 
# File    : serializers.py
# Software: PyCharm
from __future__ import unicode_literals
import logging

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.db.transaction import atomic

from main.models import StaffProfile, Hotel

logger = logging.getLogger(__name__)


class StaffProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    sex_display = serializers.CharField(
        source='get_sex_display',
        read_only=True
    )
    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True
    )
    date_joined = serializers.DateTimeField(
        source='user.date_joined',
    )
    is_active = serializers.BooleanField(
        source='user.is_active',
    )
    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    def get_groups(self, obj):
        groups = [group.name for group in list(obj.user.groups.all())]
        return groups

    class Meta:
        model = StaffProfile
        fields = (
            "id",
            "user_id",
            "user_name",
            "sex",
            "groups",
            'sex_display',
            "belong_hotel",
            "belong_hotel_name",
            'date_joined',
            'is_active',
            'username'
        )


class CreateStaffProfileSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    username = serializers.CharField(
        source='user.username'
    )

    belong_hotel_name = serializers.CharField(
        source='belong_hotel.name',
        read_only=True,
        allow_blank=True
    )

    @atomic
    def create(self, validated_data):
        hotel = validated_data.pop('belong_hotel')

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
            'belong_hotel',
            'belong_hotel_name'
        )


class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role_id_list = serializers.ListField(
        child=serializers.IntegerField()
    )

    def create(self, validated_data):
        user_id = validated_data['user_id']
        role_list = validated_data['role_id_list']
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise serializers.ValidationError({"non_field_errors": ["用户ID传递错误"]})
        group_list = list(Group.objects.filter(id__in=role_list))
        user.groups.set(group_list)
        return validated_data

