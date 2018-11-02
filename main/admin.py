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

    list_display = ['order_type', 'order_id', 'order_status', 'belong_hotel', 'pay_type', 'consumer']


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'goods_name', 'is_integral', 'is_special']


class ConsumerBalanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'consumer', 'balance_type', 'message']

admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Goods, GoodsAdmin)
admin.site.register(models.ConsumerBalance, ConsumerBalanceAdmin)

for attr in dir(models):
    model = getattr(models, attr)

    if not inspect.isclass(model):
        continue
    try:
        admin.site.register(model)
    except:
        pass
