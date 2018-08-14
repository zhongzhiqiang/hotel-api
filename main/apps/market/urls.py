# coding:utf-8

from rest_framework import routers
from main.apps.market import views


router = routers.DefaultRouter()
# router.register('goods_list', views.GoodsList, base_name='goods')
router.register('goods_category', views.GoodsCategoryView, base_name='goods_category')
router.register('goods_list', views.GoodsView, base_name='goods_views')
urlpatterns = router.urls
