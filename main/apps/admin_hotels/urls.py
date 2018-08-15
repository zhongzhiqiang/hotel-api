# coding:utf-8
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_hotels import views


router = routers.DefaultRouter()
router.register('hotel', views.AdminHotelView, base_name='hotel')

urlpatterns = router.urls
