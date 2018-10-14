# coding:utf-8
# Time    : 2018/10/14 下午7:14
# Author  : Zhongzq
# Site    : 
# File    : seriliazer_fields.py
# Software: PyCharm
from __future__ import unicode_literals
from rest_framework import serializers


class ImageField(serializers.CharField):
    def to_representation(self, value):
        if isinstance(value, basestring):
            return eval(value)
        return value


class TagsField(serializers.CharField):
    def to_representation(self, value):
        if isinstance(value, basestring):
            return eval(value)
        return value
