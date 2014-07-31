# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Picture(models.Model):
    user = models.ForeignKey('account.User', verbose_name=_(u'Пользователь'))
    title = models.CharField(_(u'Наименование'), max_length=250)
    picture = models.ImageField(_(u'Картинка'), upload_to='%Y/%m_%d')
    creation_date = models.DateTimeField(
        _(u'Дата создания'), auto_now_add=True)

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _(u'Картинка')
        verbose_name_plural = _(u'Картинки')
