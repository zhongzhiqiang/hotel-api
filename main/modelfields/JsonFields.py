# coding:utf-8
# Time    : 2018/8/23 下午3:21
# Author  : Zhongzq
# Site    : 
# File    : JsonFields.py
# Software: PyCharm
from __future__ import unicode_literals

from django import VERSION

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import six

# Try to be compatible with Django 1.5+.
try:
    import json
except ImportError:
    from django.utils import simplejson as json

# Basestring no longer exists in Python 3
try:
    basestring
except Exception:
    basestring = str

if VERSION >= (1, 8):
    JSONFieldBase = models.TextField
else:
    JSONFieldBase = six.with_metaclass(models.SubfieldBase, models.TextField)


class JSONField(JSONFieldBase):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478
    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)
        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """

    def to_python(self, value):
        """
        Convert a string from the database to a Python value.
        """
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
            elif isinstance(value, bytes):
                return json.loads(value.decode('utf8'))
        except ValueError:
            pass
        return value

    def get_prep_value(self, value):
        """
        Convert the value to a string so it can be stored in the database.
        """
        value = super(JSONField, self).get_prep_value(value)
        if value == "":
            return None
        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value, cls=DjangoJSONEncoder, sort_keys=True, indent=2, separators=(',', ': '))
        return value

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def get_default(self):
        # Override Django's `get_default()` to avoid stringification.
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        return ""

    def get_db_prep_save(self, value, *args, **kwargs):
        value = super(JSONField, self).get_db_prep_save(value, *args, **kwargs)

        if value == "":
            return None

        if isinstance(value, dict) or isinstance(value, list):
            return json.dumps(value, cls=DjangoJSONEncoder, sort_keys=True, indent=2, separators=(',', ': '))
        else:
            return value

    def value_from_object(self, obj):
        value = super(JSONField, self).value_from_object(obj)
        if self.null and value is None:
            return None
        return json.dumps(value, sort_keys=True, indent=2, separators=(',', ': '))
