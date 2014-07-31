# -*- coding: utf-8 -*-

from django.contrib.auth.models import UserManager


class EmailAsUsernameManager(UserManager):
    def make_username(self, email):
        username = email.split('@')[0]
        qty = self.filter(username__istartswith=username).count()
        return '{}_{}'.format(username, qty)

    def _create_user(self, username=None, email=None, password=None,
                     is_staff=False, is_superuser=False, **extra_fields):

        if not username:
            username = self.make_username(email)

        return super(EmailAsUsernameManager, self)._create_user(
            username, email, password, is_staff, is_superuser, **extra_fields)

    def create_user(self, *args, **kwargs):
        return self._create_user(*args, **kwargs)

    def create_superuser(self, *args, **kwargs):
        kwargs['is_staff'], kwargs['is_superuser'] = True, True
        return self._create_user(*args, **kwargs)
