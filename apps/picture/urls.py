# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'picture', views.PictureViewSet)

urlpatterns = patterns(
    '',

    url(r'^', include(router.urls)),
)
