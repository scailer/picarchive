# -*- coding: utf-8 -*-

from rest_framework import serializers
from utils.rest import fields
from . import models


class PictureSerializer(serializers.ModelSerializer):
    picture = fields.ImageBase64Field(source='picture')
    notice = serializers.SerializerMethodField('_notice')
    is_owner = serializers.SerializerMethodField('_is_owner')

    def _get_user(self):
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated():
            return request.user

    def _notice(self, obj):
        if not obj:
            return

        if self._get_user():
            notice = obj.notice_set.filter(user=self._get_user())
            return '<br>'.join(notice.values_list('text', flat=True))

    def _is_owner(self, obj):
        if not obj:
            return

        return getattr(self._get_user(), 'pk', None) == obj.user.pk


    class Meta:
        model = models.Picture
        read_only_fields = ('user',)
