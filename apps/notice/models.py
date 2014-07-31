# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Notice(models.Model):
    text = models.TextField(_(u'Заметка'))
    user = models.ForeignKey('account.User', verbose_name=_(u'Пользователь'))
    picture = models.ForeignKey('picture.Picture', verbose_name=_(u'Картинка'))
    creation_date = models.DateTimeField(
        _(u'Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _(u'Заметка')
        verbose_name_plural = _(u'Заметки')
