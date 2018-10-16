# coding:utf-8
# Time    : 2018/10/16 下午12:20
# Author  : Zhongzq
# Site    : 
# File    : CompressionImageField.py
# Software: PyCharm
from __future__ import unicode_literals
import cStringIO

from django.db.models import  ImageField
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile

try:
    from PIL import Image, ImageOps
except:
    # Mac OSX
    import Image, ImageOps


# 这里建议按比例压缩。
def generate_thumb(original, format='JPEG'):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail

    Arguments:
    original -- The image being resized as `File`.
    size     -- Desired thumbnail size as `tuple`. Example: (70, 100)
    format   -- Format of the original image ('JPEG', 'PNG', ...) The thumbnail will be generated using this same format.

    """
    original.seek(0)  # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(original)

    # 这里表示小于200kb的不压缩
    if len(original) / 1024 < 200:
        return original

    # 这里表示大于200kb 需要压缩
    ratio = int(len(original) / 1024 / 200)

    width = int(image.width / ratio)
    height = int(image.height / ratio)
    # 这里将图片减少y
    if image.mode not in ('L', 'RGB', 'RGBA'):
        image = image.convert('RGB')
    thumbnail = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
    io = cStringIO.StringIO()
    if format.upper() == 'JPG':
        format = 'JPEG'
    thumbnail.save(io, format)
    return ContentFile(io.getvalue())


class ImageCompressionFieldFile(ImageFieldFile):
    def __init__(self, *args, **kwargs):
        super(ImageCompressionFieldFile, self).__init__(*args, **kwargs)

    def save(self, name, content, save=True):
        content = generate_thumb(content)
        super(ImageCompressionFieldFile, self).save(name, content, save)


class CompressionImageField(ImageField):
    attr_class = ImageCompressionFieldFile

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.verbose_name = verbose_name
        self.name = name
        self.width_field = width_field
        self.height_field = height_field
        super(ImageField, self).__init__(**kwargs)
