#!/usr/bin/env python
# encoding: utf-8

from rest_framework import serializers

from django.contrib.auth.models import Group, Permission
from django.db import transaction
from rest_framework.validators import UniqueValidator


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
            'content_type',
            'codename',
        )
        read_only_fields = ('id',)


class RoleSerializer(serializers.ModelSerializer):

    permissions_info = PermissionSerializer(
        read_only=True,
        many=True,
        source="permissions",
    )
    perms = serializers.SerializerMethodField()

    def get_perms(self, obj):
        return list(obj.permissions.all().values_list('codename', flat=True))

    user_ids = serializers.SerializerMethodField()

    def get_user_ids(self, obj):
        return list(obj.user_set.all().values_list('id', flat=True))

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'permissions',
            'permissions_info',
            'perms',
            'user_ids',
        )
        read_only_fields = ('id',)


class CreateRoleSerializer(serializers.ModelSerializer):

    perms = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        allow_empty=False,
        error_messages={'empty': u'请选择权限'},
    )

    def create(self, validated_data):
        perms = validated_data.pop('perms', [])
        with transaction.atomic():
            group = super(CreateRoleSerializer, self).create(validated_data)
            permissions = list(Permission.objects.filter(codename__in=perms))
            group.permissions.set(permissions)
        return group

    @transaction.atomic
    def update(self, instance, validated_data):
        perms = validated_data.pop('perms', [])

        group = super(CreateRoleSerializer, self).update(instance, validated_data)
        permissions = list(Permission.objects.filter(codename__in=perms))
        group.permissions.set(permissions)
        return group

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'perms',
        )
        extra_kwargs = {
            'name': {
                'validators': [
                    UniqueValidator(Group.objects.all(), message=u'该名称已被占用'),
                ],
                'error_messages': {
                    'null': u'请填写角色名称',
                    'blank': u'请填写角色名称',
                    'required': u'请填写角色名称',
                }
            },
        }
