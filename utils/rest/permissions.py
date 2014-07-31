# -*- coding: utf-8 -*-

from utils import rec_getattr
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Запрещает редактировать ресурсы которые не пренадлежат владельцу.
    Поле принадлежности во View - owner_id_source
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.method in permissions.SAFE_METHODS or
                    request.user and request.user.is_authenticated() and
                    request.user.id == rec_getattr(obj, view.owner_id_source))


class IsOwnerOnly(permissions.BasePermission):
    """
    Только для владельца
    owner_id_source
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated() and
                    request.user.id == rec_getattr(obj, view.owner_id_source))


class CanDelete(permissions.BasePermission):
    """
        Разрешает удаление, только при наличии Django permission
    """

    def has_object_permission(self, request, view, obj):
        if view.action != 'destroy':
            return True

        model_cls = getattr(view, 'model', None)
        queryset = getattr(view, 'queryset', None)

        if model_cls is None and queryset is not None:
            model_cls = queryset.model

        assert model_cls, ('Cannot apply CanDelete on a view that does'
                           'not have `.model` or `.queryset` property.')

        perm = '{0}.delete_{1}'.format(
            model_cls._meta.app_label,
            model_cls._meta.module_name
        )

        return request.user.has_perm(perm)


class DjangoPermissionsWithActions(permissions.DjangoModelPermissions):
    action_to_perm_map = {
        'update': 'change',
        'create': 'add',
        'retrieve': 'view',
        'partial_update': 'change',
        'destroy': 'delete',
    }

    def get_required_permissions(self, action, model_cls):
        app_label = model_cls._meta.app_label
        model_name = model_cls._meta.module_name
        action = self.action_to_perm_map.get(action, action)
        return '{app_label}.{action}_{model_name}'.format(**locals())

    def has_object_permission(self, request, view, obj):
        model_cls = getattr(view, 'model', None)
        queryset = getattr(view, 'queryset', None)

        if model_cls is None and queryset is not None:
            model_cls = queryset.model

        return request.user.has_perms(
            self.get_required_permissions(view.action, model_cls))


class IsOwnerOrDjangoPermissions(DjangoPermissionsWithActions):
    def has_object_permission(self, request, view, obj):
        if (request.user and request.user.is_authenticated() and
            request.user.id == rec_getattr(obj, view.owner_id_source)):
            return True

        return super(IsOwnerOrDjangoPermissions, self
                     ).has_object_permission(request, view, obj)
