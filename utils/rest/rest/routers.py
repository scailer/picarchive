# -*- coding: utf-8 -*-

from rest_framework.routers import DefaultRouter, Route


class SchemaRouter(DefaultRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Schema description router
        Route(
            url=r'^{prefix}/schema$',
            mapping={
                'get': 'schema'
            },
            name='{basename}-schema',
            initkwargs={'suffix': 'Schema'}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated routes.
        # Generated using @action or @link decorators on methods of the viewset
        Route(
            url=r'^{prefix}/{lookup}/{methodname}$',
            mapping={
                '{httpmethod}': '{methodname}',
            },
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]
