# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from . import managers


class User(AbstractUser):
    """ Пользователь """

    objects = managers.EmailAsUsernameManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        return super(User, self).get_full_name() or self.email.split('@')[0]

    class Meta:
        verbose_name = _(u'Пользователь')
        verbose_name_plural = _(u'Пользователь')


User._meta.get_field_by_name('email')[0]._unique = True
