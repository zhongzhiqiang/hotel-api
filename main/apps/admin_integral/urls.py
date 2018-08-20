# coding:utf-8
from __future__ import unicode_literals

from rest_framework import routers

from main.apps.admin_integral import views

router = routers.DefaultRouter()
router.register('integral', views.UserIntegralView, base_name='integral')

urlpatterns = router.urls