# coding:utf-8

from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_market import views

router = routers.DefaultRouter()

router.register('goods', views.GoodsView, base_name='goods')
router.register('goods_category', views.GoodsCategoryView, base_name='goods_category')

urlpatterns = router.urls