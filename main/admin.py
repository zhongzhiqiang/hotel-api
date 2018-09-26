# coding:utf-8
import inspect

from django.contrib import admin
from main import models


class MarketOrderDetailAdmin(admin.TabularInline):
    model = models.MarketOrderDetail


class MarketOrderAdmin(admin.ModelAdmin):
    inlines = [MarketOrderDetailAdmin]

admin.site.register(models.Goods)
admin.site.register(models.GoodsCategory)
admin.site.register(models.Hotel)
admin.site.register(models.Consumer)
admin.site.register(models.IntegralDetail)
admin.site.register(models.Integral)
admin.site.register(models.IntegralSettings)
admin.site.register(models.GrowthValueSettings)
admin.site.register(models.RoomStyles)
admin.site.register(models.Rooms)
admin.site.register(models.HotelOrderRoomInfo)
admin.site.register(models.HotelOrder)
admin.site.register(models.HotelOrderDetail)
admin.site.register(models.MarketOrder, MarketOrderAdmin)

for attr in dir(models):
    model = getattr(models, attr)

    if not inspect.isclass(model):
        continue
    try:
        admin.site.register(model)
    except:
        pass
