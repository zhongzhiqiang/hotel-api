# coding:utf-8
import inspect

from django.contrib import admin
from main import models


class HotelOrderInline(admin.TabularInline):
    model = models.HotelOrderDetail


class MarketOrderInline(admin.TabularInline):
    model = models.MarketOrderDetail


class MarketOrderContactInline(admin.TabularInline):
    model = models.MarketOrderContact


class OrderPayInline(admin.TabularInline):
    model = models.OrderPay


class OrderAdmin(admin.ModelAdmin):
    inlines = [HotelOrderInline, MarketOrderContactInline, MarketOrderInline, OrderPayInline]


admin.site.register(models.Order, OrderAdmin)


for attr in dir(models):
    model = getattr(models, attr)

    if not inspect.isclass(model):
        continue
    try:
        admin.site.register(model)
    except:
        pass
