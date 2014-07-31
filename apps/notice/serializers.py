# -*- coding: utf-8 -*-

from rest_framework import serializers
from . import models


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notice
        read_only_fields = ('user',)
