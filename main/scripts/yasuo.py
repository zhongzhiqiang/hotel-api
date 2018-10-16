# coding:utf-8
# Time    : 2018/10/16 上午11:21
# Author  : Zhongzq
# Site    : 
# File    : yasuo.py
# Software: PyCharm
from __future__ import unicode_literals
import sys
sys.path.append('../../')
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from main.models import Images

from django_thumbs.db.models import generate_thumb

THUMB_SUFFIX = '%s.%sx%s.%s'
images_list = Images.objects.all()

for image in images_list:
    p = image.image.path

    with open(p) as f:
        content = generate_thumb(f, (200, 200))

        name, b = image.image.name.rsplit('.')
        new_name = THUMB_SUFFIX % (name, 200, 200, b)

        image.image.storage.save(new_name, content)


