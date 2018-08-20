# coding:utf-8

from django.contrib import admin
from main import models

admin.site.register(models.Goods)
admin.site.register(models.GoodsCategory)
admin.site.register(models.Hotel)
admin.site.register(models.Consumer)
admin.site.register(models.IntegralDetail)
admin.site.register(models.Integral)
admin.site.register(models.IntegralSettings)
admin.site.register(models.GrowthValueSettings)

