# -*- coding: utf-8 -*-

from rest_framework import viewsets, permissions
from utils.rest import mixins
from . import models
from . import serializers


class NoticeViewSet(mixins.OwnerViewSetMixin, viewsets.ModelViewSet):
    model = models.Notice
    model_serializer_class = serializers.NoticeSerializer
    serializer_class = serializers.NoticeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = super(NoticeViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)
