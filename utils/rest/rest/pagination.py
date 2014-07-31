# -*- coding: utf-8 -*-

from rest_framework import pagination
from rest_framework import serializers


class CurrentPageField(serializers.Field):
    def to_native(self, value):
        return value.number


class PaginationSerializer(pagination.PaginationSerializer):
    page = CurrentPageField(source='*')
    count = serializers.Field(source='paginator.count')
    per_page = serializers.Field(source='paginator.per_page')
    pages = serializers.Field(source='paginator.num_pages')
