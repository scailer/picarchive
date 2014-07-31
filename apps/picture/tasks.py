# -*- coding: utf-8 -*-

from celery.task import task
from utils import logger
from utils.zip import InMemoryZip
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@task(name='send_pictures')
def send_pictures(email, picture_pk_list):
    from apps.picture.models import Picture

    pictures = Picture.objects.filter(pk__in=picture_pk_list)
    imz = InMemoryZip()

    for pic in pictures:
        name = '{}.{}'.format(pic.id, pic.picture.name.split('.')[-1])
        imz.append(name, pic.picture.read())

    imz.finalize()

    msg = EmailMultiAlternatives(
        u'Подборка картинок', '',
        settings.DEFAULT_FROM_EMAIL,
        [email])
    msg.attach_alternative(imz.in_memory_data.getvalue(), "application/zip")
    msg.send()

    logger.info('Send mail to {}'.format(email))
