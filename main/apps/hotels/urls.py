# coding:utf-8

from rest_framework import routers

from main.apps.hotels import views

router = routers.DefaultRouter()
router.register('hotel', views.HotelView, base_name='hotel')

urlpatterns = router.urls
