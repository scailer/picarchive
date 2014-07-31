# -*- coding: utf-8 -*-

from rest_framework import viewsets, fields, relations
from rest_framework.response import Response
from rest_framework.reverse import reverse
from utils.rest import fields as local_fields


FILTER_TYPE_MAP = {
    'MultiFieldCharFilter': 'TextField',
    'DateRangeFilter': 'SelectField',
    'ModelChoiceFilter': 'ForeignKeyField',
    'ModelMultipleChoiceFilter': 'ForeignKeyField',
    'ListRetrieveFilter': None,
    'ChoiceFilter': 'SelectField',
}


class SchemaMixin(object):
    def filters(self, request, *args, **kwargs):
        filters = {}

        if not getattr(self, 'filter_fields', None):
            return filters

        for f_name in self.filter_fields:
            field = None

            for backend in self.filter_backends:
                field = backend.default_filter_set.base_filters.get(f_name)

                if field:
                    break

            if not field:
                continue

            field_type = FILTER_TYPE_MAP.get(field.__class__.__name__)

            if not field_type:
                continue

            data = {
                'name': f_name,
                'label': unicode(field.label),
                'type': field_type,
            }

            if field_type == 'SelectField':
                choices = field.field.choices
                data['choices'] = [{'label': unicode(v),
                                    'value': k}
                                   for k, v in choices]

            if field_type == 'ForeignKeyField':
                data['model'] = field.field.queryset.model.__name__
                view_name = '{}-list'.format(data['model'].lower())
                data['resource_url'] = reverse(view_name)

            filters[f_name] = data

        return filters

    def schema(self, request, *args, **kwargs):
        srlz = self.get_serializer_class()()

        reverse_prop = dict([(v, k) for k, v in srlz.fields.items()])
        model_fields = dict([(x.name, x) for x in srlz.Meta.model._meta.fields
                             + srlz.Meta.model._meta.many_to_many])

        def _scan_field(f):
            data = {
                'type': f.type_name or f.__class__.__name__,
                'name': reverse_prop[f],
                'default': None,
                'label': hasattr(f, 'label') and unicode(f.label) or '',
            }

            if getattr(f, 'default', False):
                data['default'] = f.default

            if isinstance(f, fields.ChoiceField):
                data['choices'] = [{'label': unicode(v),
                                    'value': k}
                                   for k, v in f.choices]

            if isinstance(f, relations.RelatedField):
                view_name = '{}-list'.format(
                    f.queryset.model.__name__.lower())
                data['resource_url'] = reverse(view_name)
                data['model'] = f.queryset.model.__name__

            if isinstance(f, local_fields.ListField):
                view_name = '{}-list'.format(
                    f.serializer_class.Meta.model.__name__.lower())
                data['resource_url'] = reverse(view_name)
                data['label'] = f.label
                data['model'] = f.serializer_class.Meta.model.__name__

            name = reverse_prop[f]
            data['name'] = name
            model_field_name = getattr(f, 'source', name) or name

            if model_field_name in model_fields:
                mf = model_fields[model_field_name]
                if hasattr(f, 'label'):
                    data['label'] = unicode(f.label or mf.verbose_name)
                data['required'] = getattr(f, 'required', not mf.blank)

                if data['type'] == 'CharField':
                    data['type'] = mf.__class__.__name__

            if f.read_only:
                data['read_only'] = f.read_only

            return data

        res = {
            'name': srlz.__class__.__name__,
            'description': srlz.__doc__,
            'type': 'object',
            'fields': dict([(k, _scan_field(v))
                            for k, v in srlz.fields.items()])
        }

        return Response(res)

    def sorts(self, request):
        if self.model or self.queryset:
            queryset = self.get_queryset()
            return [x.name for x in queryset.model._meta.fields]

        return []

    def metadata(self, request):
        opt = super(SchemaMixin, self).metadata(request)
        opt['schema'] = self.schema(request).data
        opt['filters'] = self.filters(request)
        opt['sorts'] = self.sorts(request)
        return opt


class ModelSchemaViewSet(SchemaMixin, viewsets.ModelViewSet):
    pass
