# -*- coding: utf-8 -*-


class SortableMixin(object):
    default_sort = None
    direction_kwarg = 'sort_direction'  # asc, desc
    sort_kwarg = 'sort_name'
    sort_field_map = {}

    def get_queryset(self):
        queryset = super(SortableMixin, self).get_queryset()
        sort_field = self.request.REQUEST.get(self.sort_kwarg)
        direction = self.request.REQUEST.get(self.direction_kwarg, 'asc')
        fields = [x.name for x in queryset.model._meta.fields]

        if not sort_field or not sort_field in fields:
            if self.default_sort:
                return queryset.order_by(*self.default_sort)
            else:
                return queryset

        sort_field = self.sort_field_map.get(sort_field, sort_field)
        direction = {'asc': '', 'desc': '-'}.get(direction, '')
        return queryset.order_by(direction + sort_field)


class OwnerViewSetMixin(object):
    def get_serializer(self, instance=None, data=None,
                       files=None, many=False, partial=False):

        if not instance and self.action == 'create':
            instance = self.model(user=self.request.user)

        return super(OwnerViewSetMixin, self).get_serializer(
            instance, data=data, files=files, many=many, partial=partial)
