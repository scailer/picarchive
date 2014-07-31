# -*- coding: utf-8 -*-

import re
import json
import uuid

from base64 import decodestring
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail
from rest_framework import serializers

img_parser = re.compile(r'data:image/(\w+);base64,([\w+/=]+)')


class ListField(serializers.Field):
    type_name = 'MultipleField'

    def __init__(self, source, serializer_class, label=None, type_name=None):
        super(ListField, self).__init__()
        self.label = label
        self.source = source
        self.serializer_class = serializer_class
        self.type_name = type_name or self.type_name

    def field_to_native(self, obj, field_name):
        if not obj:
            return []

        field = getattr(obj, self.source)

        try:
            queryset = field.all()
        except AttributeError:
            queryset = field

        return self.serializer_class(queryset, many=True).data


class StaticField(serializers.Field):
    read_only = True
    type_name = 'StaticField'

    def __init__(self, value):
        super(StaticField, self).__init__()
        self.value = value

    def field_to_native(self, obj, field_name):
        return self.value


def _fix_url(url):
    return url.split('?')[0]


class ImageBase64Field(serializers.ImageField):
    type_name = 'ImageField'

    def from_native(self, data):
        if not data:
            return None

        res = img_parser.match(data.get('url', ''))
        if res:
            filetype, data = res.groups()
        else:
            return data.get('related', '')

        data = decodestring(data)
        filename = 'pic_{}.{}'.format(uuid.uuid1().hex[:8], filetype)
        f = ContentFile(data, name=filename)

        return super(ImageBase64Field, self).from_native(f)

    def to_native(self, value):
        if not value:
            return None

        return {
            'url': _fix_url(value.url),
            'related': value.name,
            'preview': _fix_url(get_thumbnail(
                value, '250x250', crop='center').url)
        }


class ForeignKeyField(serializers.PrimaryKeyRelatedField):
    def __init__(self, *args, **kwargs):
        self.serializer_class = kwargs.pop('serializer_class')
        super(ForeignKeyField, self).__init__(*args, **kwargs)

    def from_native(self, data):
        if isinstance(data, unicode):
            data = eval(data)
        return super(ForeignKeyField, self).from_native(data.get('id', None))

    def to_native(self, pk):
        return self.serializer_class(self.queryset.get(pk=pk)).data


class JSONField(serializers.WritableField):
    pass


class MultipleField(ForeignKeyField):
    def __init__(self, *args, **kwargs):
        kwargs['many'] = True
        super(MultipleField, self).__init__(*args, **kwargs)


class CreateRelatedField(MultipleField):
    def from_native(self, data):
        try:
            val = int(data.get('id'))

        except (TypeError, ValueError):
            srlz = self.serializer_class(data=data)

            if srlz.is_valid():
                srlz.save()
                val = srlz.object.id

            else:
                val = 0

        return super(ForeignKeyField, self).from_native(val)
