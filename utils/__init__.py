# -*- coding: utf-8 -*-

import logging
from django.db.models.fields.files import FieldFile

logger = logging.getLogger('project')
refetch = lambda obj: obj.__class__.objects.get(pk=obj.pk)


def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def or_Q(lst):
    # or func for iterable for Q-objects
    q = lst and lst[0] or None
    for x in lst[1:]:
        q = q | x
    return q


def diff(instance1, instance2):
    assert type(instance1) == type(instance2), ('Instances must be same type')
    res = {}

    keys = [k for k, v in instance1.__dict__.items() if k[0] != '_']
    data1, data2 = instance1.__dict__, instance2.__dict__

    for key in keys:
        value1 = data1.get(key)
        value2 = data2.get(key)

        if isinstance(value1, FieldFile) or isinstance(value2, FieldFile):
            continue

        if value1 != value2:
            res[key] = (value1, value2)

    return res


def rec_getattr(obj, attr):
    """ Рекурсивный getattr: rec_getattr(request, 'user.id') """
    if '.' not in attr:
        return getattr(obj, attr)
    else:
        L = attr.split('.')
        return rec_getattr(getattr(obj, L[0]), '.'.join(L[1:]))


def rec_get(obj, key):
    """ Рекурсивный get: rec_get(dict, 'user.id') """
    if "." not in key:
        return obj[key]  # Нужен явный KeyError
    else:
        L = key.split('.')
        return rec_get(obj[L[0]], '.'.join(L[1:]))
