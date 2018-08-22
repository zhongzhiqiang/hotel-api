# coding:utf-8
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_hotels import views


router = routers.DefaultRouter()
router.register('hotel', views.AdminHotelView, base_name='hotel')
router.register('room_style', views.AdminRoomStyle, base_name='room_style')

urlpatterns = router.urls
