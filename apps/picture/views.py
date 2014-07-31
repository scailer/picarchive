# -*- coding: utf-8 -*-

from rest_framework import viewsets, renderers
from utils.rest import mixins, permissions
from . import models
from . import serializers
from . import renderers as local_renderers


class PictureViewSet(mixins.OwnerViewSetMixin, viewsets.ModelViewSet):
    owner_id_source = 'user.pk'
    model = models.Picture
    model_serializer_class = serializers.PictureSerializer
    serializer_class = serializers.PictureSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    renderer_classes = (
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        local_renderers.SendToMailRenderer
    )
