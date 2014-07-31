# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)

urlpatterns = patterns(
    '',

    url(r'^', include(router.urls)),
    url(r'^login$', views.LoginView.as_view(), name="login"),
    url(r'^logout$', views.LogoutView.as_view(), name="logout"),
    url(r'^registration$', views.RegistrationView.as_view(),
        name="registration"),
)
